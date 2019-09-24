from flask_restful import Resource, Api, fields, marshal_with
from fllipit import APP
from models import DB, Team
import pypyodbc

API = Api(APP)


# Get teams from the database
def getTeams():
    teams = []
    if APP.config['TEST_DB']:
        # In test mode, use the sqlite database
        teams = Team.query.all()
        for team in teams:
            team.sortScores()
    else:
        # In production mode, get the data from the Access database
        # Create the database connection
        conn = pypyodbc.connect(
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
            r"Dbq=" + APP.config['DB_FILE'] + ";")
        cur = conn.cursor()

        # Get the data from the database
        cur.execute(
            '''
            SELECT TeamNumber, 
            TeamName, 
            Affiliation,
            Trial1Score, 
            Trial2Score, 
            Trial3Score,
            Trial4Score, 
            Trial5Score,
            Trial6Score,
            Trial7Score,
            ToRound4, 
            ToRound5,
            ToRound6, 
            ToRound7,
            Trial1PenaltyCount, 
            Trial2PenaltyCount, 
            Trial3PenaltyCount, 
            Trial4PenaltyCount,
            Trial5PenaltyCount, 
            playoffsround1score,
            playoffsround2score, 
            playoffsround3score, 
            playoffsround4score,
            playoffsround1penaltycount,
            playoffsround2penaltycount, 
            playoffsround3penaltycount, 
            playoffsround4penaltycount
            FROM ScoringSummaryQuery
            ''')

        # Build the list of Team objects
        for row in cur.fetchall():
            # Build the team object
            team = Team(
                number=row[0],
                name=row[1],
                affiliation=row[2],
                round1=row[3],
                round2=row[4],
                round3=row[5],
                round4=row[6],
                round5=row[7],
                round6=row[8],
                round7=row[9],
                advanceTo4=row[10]=='Yes',
                advanceTo5=row[11]=='Yes',
                advanceTo6=row[12]=='Yes',
                advanceTo7=row[13]=='Yes',
                round1Penalties=row[14],
                round2Penalties=row[15],
                round3Penalties=row[16],
                round4Penalties=row[17],
                round5Penalties=row[18],
                elim1=row[19],
                elim2=row[20],
                elim3=row[21],
                elim4=row[22],
                elim1Penalties=row[23],
                elim2Penalties=row[24],
                elim3Penalties=row[25],
                elim4Penalties=row[26] )

            # Add the current team to the list of all teams
            teams.append(team)

        # Close the database connection
        cur.close()
        conn.close()
    
    return teams

def rankTeams(teams):
    return sorted(
        teams,
        key=lambda x: (x.bestScore, x.secondBestScore, x.worstScore, -x.bestScorePenalties, -x.secondBestScorePenalties, -x.worstScorePenalties),
        reverse=True)


# Setup the fields that will be used in the JSON output
teamFields = {
    "number": fields.Integer,
    "name": fields.String,
    "affiliation": fields.String,
    "round1": fields.Integer,
    "round2": fields.Integer,
    "round3": fields.Integer,
    "round4": fields.Integer,
    "round5": fields.Integer,
    "bestScore": fields.Integer,
    "rank": fields.Integer
}


playoffFields = {
    "number": fields.Integer,
    "name": fields.String,
    "score": fields.Integer
}


class Rankings(Resource):

    """Setup a REST resource for the Team data."""

    @marshal_with(teamFields)
    def get(self):
        teams = getTeams()
        rankedTeams = rankTeams(teams)
             
        i = 1
        for team in rankedTeams:
            team.rank = i
            i += 1
        
        return rankedTeams


class Playoffs(Resource):
    
    """Setup a REST resource for the playoff data"""
    
    @marshal_with(playoffFields)
    def get(self, roundNumber):
        # Get only the teams that are marked to advance to the selected round
        teams = [t for t in getTeams() if t.isAdvancingToRound(roundNumber)]
        
        # Add a temporary attribute 'score' to the team objects, for generic REST output
        for team in teams:
            team.score = team.getRoundScore(roundNumber)

        # Return team list sorted by scores from previous round
        return sorted(
            teams,
            key=lambda x: (x.getRoundScore(roundNumber), -x.getRoundPenalties(roundNumber)),
            reverse=True)

class TournamentSettings(Resource):

    """Setup a REST resource for the tournament settings"""

    def get(self):
        rounds = 3
        if(APP.config['USE_5_QUAL_ROUNDS']):
            rounds = 5

        return {'qualifying_rounds': rounds}


        

# map resource to URL
API.add_resource(Rankings, '/api/teams')
API.add_resource(Playoffs, '/api/playoffs/<int:roundNumber>')
API.add_resource(TournamentSettings, '/api/settings')