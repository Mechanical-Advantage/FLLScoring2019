from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Team(DB.Model):
    """Store data for a single Team"""
    number = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(200), unique=True)
    affiliation = DB.Column(DB.String(200), unique=True)
    round1 = DB.Column(DB.Integer)
    round2 = DB.Column(DB.Integer)
    round3 = DB.Column(DB.Integer)
    round4 = DB.Column(DB.Integer)
    round5 = DB.Column(DB.Integer)
    advanceTo4 = DB.Column(DB.Boolean)
    advanceTo5 = DB.Column(DB.Boolean)
    advanceTo6 = DB.Column(DB.Boolean)
    advanceTo7 = DB.Column(DB.Boolean)
    round1Penalties = DB.Column(DB.Integer)
    round2Penalties = DB.Column(DB.Integer)
    round3Penalties = DB.Column(DB.Integer)
    round4Penalties = DB.Column(DB.Integer)
    round5Penalties = DB.Column(DB.Integer)
    elim1 = DB.Column(DB.Integer)
    elim2 = DB.Column(DB.Integer)
    elim3 = DB.Column(DB.Integer)
    elim4 = DB.Column(DB.Integer)
    elim1Penalties = DB.Column(DB.Integer)
    elim2Penalties = DB.Column(DB.Integer)
    elim3Penalties = DB.Column(DB.Integer)
    elim4Penalties = DB.Column(DB.Integer)

    # Constructor for the object
    def __init__(
        self,
        number=1234,
        name='MyTeam',
        affiliation="MyOrganizaton",
        round1=0,
        round2=0,
        round3=0,
        round4=0,
        round5=0,
        round6=0,
        round7=0,
        advanceTo4=False,
        advanceTo5=False,
        advanceTo6=False,
        advanceTo7=False,
        round1Penalties=0,
        round2Penalties=0,
        round3Penalties=0,
        round4Penalties=0,
        round5Penalties=0,
        elim1=0,
        elim2=0,
        elim3=0,
        elim4=0,
        elim1Penalties=0,
        elim2Penalties=0,
        elim3Penalties=0,
        elim4Penalties=0,
    ):
        """Construct a Team object using a name and URL."""
        self.number = number
        self.name = name
        self.affiliation = affiliation
        self.round1 = round1
        self.round2 = round2
        self.round3 = round3
        self.round4 = round4
        self.round5 = round5
        self.advanceTo4 = advanceTo4
        self.advanceTo5 = advanceTo5
        self.advanceTo6 = advanceTo6
        self.advanceTo7 = advanceTo7
        self.round1Penalties = round1Penalties
        self.round2Penalties = round2Penalties
        self.round3Penalties = round3Penalties
        self.round4Penalties = round4Penalties
        self.round5Penalties = round5Penalties
        self.elim1 = elim1
        self.elim2 = elim2
        self.elim3 = elim3
        self.elim4 = elim4
        self.elim1Penalties = elim1Penalties
        self.elim2Penalties = elim2Penalties
        self.elim3Penalties = elim3Penalties
        self.elim4Penalties = elim4Penalties
        self.sortScores()

    class Score:
        def __init__(self, round=1, score=0, penalties=0):
            self.round = round
            self.score = Team.default_to_zero(score)
            self.penalties = Team.default_to_zero(penalties)

    def sortScores(self):
        scores = [self.Score(1, self.round1, self.round1Penalties),
                  self.Score(2, self.round2, self.round2Penalties),
                  self.Score(3, self.round3, self.round3Penalties),
                  self.Score(4, self.round4, self.round4Penalties),
                  self.Score(5, self.round5, self.round5Penalties)]
        sorted_scores = sorted(
            scores,
            key=lambda x: (x.score, -x.penalties),
            reverse=True)

        self.bestScore = sorted_scores[0].score
        self.bestScorePenalties = sorted_scores[0].penalties

        self.secondBestScore = sorted_scores[1].score
        self.secondBestScorePenalties = sorted_scores[1].penalties

        self.worstScore = sorted_scores[2].score
        self.worstScorePenalties = sorted_scores[2].penalties

    def getRoundScore(self, roundNumber):
        scores = [self.round1, self.round2, self.round3, self.round4, self.round5, self.elim1, self.elim2, self.elim3, self.elim4]
        return scores[roundNumber-1] or 0

    def getRoundPenalties(self, roundNumber):
        penalties = [
            self.round1Penalties,
            self.round2Penalties,
            self.round3Penalties,
            self.round4Penalties,
            self.round5Penalties,
            self.elim1Penalties,
            self.elim2Penalties,
            self.elim3Penalties,
            self.elim4Penalties]

        return self.default_to_zero(penalties[roundNumber-1])

    def isAdvancingToRound(self, roundNumber):
        advances = [self.advanceTo4, self.advanceTo5, self.advanceTo6, self.advanceTo7]
        return advances[roundNumber-6] == True

    @staticmethod
    def default_to_zero(number):
        if number is None:
            return 0
        else:
            return number

    def toString(self):
        """Generate a string representing the project."""
        return "%s: name=%s" % (self.number, self.name)

class scout(DB.Model):
    """Store data for a single Team"""
    team = DB.Column(DB.Integer)
    match = DB.Column(DB.Integer)
    totalscore = DB.Column(DB.Integer)
    sequence = DB.Column(DB.Integer, primary_key=True)
	# Constructor for the object
    def __init__(
        self,
        number=1234,
        name='MyTeam',
        affiliation="MyOrganizaton",
        round1=0,
        round2=0,
        round3=0,
        round4=0,
        round5=0,
        round6=0,
        round7=0,
        advanceTo4=False,
        advanceTo5=False,
        advanceTo6=False,
        advanceTo7=False,
        round1Penalties=0,
        round2Penalties=0,
        round3Penalties=0,
        round4Penalties=0,
        round5Penalties=0,
        elim1=0,
        elim2=0,
        elim3=0,
        elim4=0,
        elim1Penalties=0,
        elim2Penalties=0,
        elim3Penalties=0,
        elim4Penalties=0,
    ):
        """Construct a Team object using a name and URL."""
        self.number = number
        self.name = name
        self.affiliation = affiliation
        self.round1 = round1
        self.round2 = round2
        self.round3 = round3
        self.round4 = round4
        self.round5 = round5
        self.advanceTo4 = advanceTo4
        self.advanceTo5 = advanceTo5
        self.advanceTo6 = advanceTo6
        self.advanceTo7 = advanceTo7
        self.round1Penalties = round1Penalties
        self.round2Penalties = round2Penalties
        self.round3Penalties = round3Penalties
        self.round4Penalties = round4Penalties
        self.round5Penalties = round5Penalties
        self.elim1 = elim1
        self.elim2 = elim2
        self.elim3 = elim3
        self.elim4 = elim4
        self.elim1Penalties = elim1Penalties
        self.elim2Penalties = elim2Penalties
        self.elim3Penalties = elim3Penalties
        self.elim4Penalties = elim4Penalties
        self.sortScores()

    class Score:
        def __init__(self, round=1, score=0, penalties=0):
            self.round = round
            self.score = Team.default_to_zero(score)
            self.penalties = Team.default_to_zero(penalties)

    def sortScores(self):
        scores = [self.Score(1, self.round1, self.round1Penalties),
                  self.Score(2, self.round2, self.round2Penalties),
                  self.Score(3, self.round3, self.round3Penalties),
                  self.Score(4, self.round4, self.round4Penalties),
                  self.Score(5, self.round5, self.round5Penalties)]
        sorted_scores = sorted(
            scores,
            key=lambda x: (x.score, -x.penalties),
            reverse=True)

        self.bestScore = sorted_scores[0].score
        self.bestScorePenalties = sorted_scores[0].penalties

        self.secondBestScore = sorted_scores[1].score
        self.secondBestScorePenalties = sorted_scores[1].penalties

        self.worstScore = sorted_scores[2].score
        self.worstScorePenalties = sorted_scores[2].penalties

    def getRoundScore(self, roundNumber):
        scores = [self.round1, self.round2, self.round3, self.round4, self.round5, self.elim1, self.elim2, self.elim3, self.elim4]
        return scores[roundNumber-1] or 0

    def getRoundPenalties(self, roundNumber):
        penalties = [
            self.round1Penalties,
            self.round2Penalties,
            self.round3Penalties,
            self.round4Penalties,
            self.round5Penalties,
            self.elim1Penalties,
            self.elim2Penalties,
            self.elim3Penalties,
            self.elim4Penalties]

        return self.default_to_zero(penalties[roundNumber-1])

    def isAdvancingToRound(self, roundNumber):
        advances = [self.advanceTo4, self.advanceTo5, self.advanceTo6, self.advanceTo7]
        return advances[roundNumber-6] == True

    @staticmethod
    def default_to_zero(number):
        if number is None:
            return 0
        else:
            return number

    def toString(self):
        """Generate a string representing the project."""
        return "%s: name=%s" % (self.number, self.name)
