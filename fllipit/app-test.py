"""Backend unit testing for the FLL Pit Display."""

import unittest
import os

from coverage import coverage

from fllipit import APP, Team
from api import rankTeams


class BasicTestCase(unittest.TestCase):

    """Basic test case."""
    def test_bestScore(self):
        
        # Three scores entered
        team1 = Team(round1=350, round2=440, round3=500, round4=410, round5=120)
        team2 = Team(round1=350, round2=440, round3=120, round4=410, round5=120)
        team3 = Team(round1=350, round2=298, round3=305, round4=325, round5=120)
        team4 = Team(round1=350, round2=298, round3=305, round4=400, round5=120)
        team5 = Team(round1=250, round2=298, round3=305, round4=400, round5=410)
        
        self.assertEqual(500, team1.bestScore)
        self.assertEqual(440, team1.secondBestScore)
        self.assertEqual(410, team1.worstScore)

        self.assertEqual(440, team2.bestScore)
        self.assertEqual(410, team2.secondBestScore)
        self.assertEqual(350, team2.worstScore)

        self.assertEqual(350, team3.bestScore)
        self.assertEqual(325, team3.secondBestScore)
        self.assertEqual(305, team3.worstScore)

        self.assertEqual(400, team4.bestScore)
        self.assertEqual(350, team4.secondBestScore)
        self.assertEqual(305, team4.worstScore)

        self.assertEqual(410, team5.bestScore)
        self.assertEqual(400, team5.secondBestScore)
        self.assertEqual(305, team5.worstScore)
        
    def test_bestScore_incomplete(self):
        """Verify that the code can determine the best score for a team when not all 3 scores are entered"""
        
        # No scores entered yet
        team0 = Team()
        
        # One score entered
        team1 = Team(round1=350)
        
        # Two scores entered
        team2 = Team(round1=350, round2=440)
        team3 = Team(round1=350, round2=120)
        
        self.assertEqual(0, team0.bestScore)
        self.assertEqual(0, team0.secondBestScore)
        self.assertEqual(0, team0.worstScore)
        
        self.assertEqual(350, team1.bestScore)
        self.assertEqual(0, team1.secondBestScore)
        self.assertEqual(0, team1.worstScore)
        
        self.assertEqual(440, team2.bestScore)
        self.assertEqual(350, team2.secondBestScore)
        self.assertEqual(0, team2.worstScore)
        
        self.assertEqual(350, team3.bestScore)
        self.assertEqual(120, team3.secondBestScore)
        self.assertEqual(0, team3.worstScore)

    def test_bestScore_penlaties(self):
        """Verify that the code can determine the best score for a team when not all 3 scores are entered"""
        
        # No scores entered yet
        
        # One score entered
        team1 = Team(number=1, round1=350, round1Penalties=0)
        team2 = Team(number=2, round1=350, round1Penalties=1)
        
        teams = [team1, team2]
        sortedTeams = rankTeams(teams)
        
        self.assertEqual(sortedTeams[0].number, 1)
        self.assertEqual(sortedTeams[1].number, 2)

if __name__ == '__main__':
    unittest.main()