from os import stat_result
import pytest
from flask import Flask

from server import research_club_in_clubs_by_name
from server import research_competition_in_competitions_by_name
from server import load_competitions
from utilities.datas import load_competitions
from tests.fixtures import club_one, clubs, competition_one, competitions


def test_status_code_ok_when_logged(logged_client, mocker,
                                    club_one, competition_one):
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)
    response = logged_client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': '4'})
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data


def test_redirect_when_unlogged(client, mocker,
                                club_one, competition_one):
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)
    response = client.post('/purchasePlaces',
                           data={'competition': "Compet du printemps",
                                 'club': 'club_test1_name',
                                 'places': '4'})
    assert response.status_code == 302


def test_update_points(logged_client, mocker, competitions, competition_one,
                       club_one, captured_templates):
    mocker.patch('utilities.datas.load_competitions', return_value=competitions)
    mocker.patch('server.load_competitions', return_value=competitions)
    
    mocker.patch('server.research_competition_in_competitions_by_name',
                 return_value=competition_one)
    mocker.patch('server.research_club_in_clubs_by_name',
                 return_value=club_one)
    mocker.patch('utilities.datas.load_competitions', return_value=competitions)
    mocker.patch('server.load_competitions', return_value=competitions)
    
    response = logged_client.post('/purchasePlaces',
                                  data={'competition': "Compet du printemps",
                                        'club': 'club_test1_name',
                                        'places': '4'})
    assert response.status_code == 200    
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == 'competitions.html'
    print(context) 
