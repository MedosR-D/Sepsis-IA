#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient

import app

client = TestClient(app.app)


def test_first_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "IA": {
            "model_name": "LMW",
            "build_date": app.IA.build_date,
            "data_source": "data_sepsis 4.csv",
            "time_to_build": app.IA.time_to_build,
            "version": 0.1,
        },
        "prediction": {"total_positive": 0, "total_negative": 0, "total": 0},
    }


def test_post_positive_patient_test():
    response = client.post(
        "/predict/patient",
        json={
            "prg": 6,
            "pl": 148,
            "pr": 72,
            "sk": 35,
            "ts": 0,
            "m11": 33.6,
            "bd2": 0.627,
            "age": 50,
        },
    )

    assert response.status_code == 200
    assert response.text == '"Positive"'
    assert app.total_patient_positive == 1
    assert app.total_patient_negative == 0


def test_read_post_positive_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "IA": {
            "model_name": "LMW",
            "build_date": app.IA.build_date,
            "data_source": "data_sepsis 4.csv",
            "time_to_build": app.IA.time_to_build,
            "version": 0.1,
        },
        "API": {
            "average_preditction_response_time": round(
                round(app.time_to_predict.total_seconds() * 1000, 2)
                / (app.total_patient_negative + app.total_patient_positive),
                2,
            )
        },
        "prediction": {"total_positive": 1, "total_negative": 0, "total": 1},
    }


def test_post_noborn_patient_test():

    age_tested = -6

    response = client.post(
        "/predict/patient",
        json={
            "prg": 1,
            "pl": 189,
            "pr": 60,
            "sk": 23,
            "ts": 846,
            "m11": 30.1,
            "bd2": 0.398,
            "age": age_tested,
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than",
                "loc": ["body", "age"],
                "msg": "Input should be greater than 0",
                "input": age_tested,
                "ctx": {"gt": 0},
            }
        ]
    }
    assert app.total_patient_positive == 1
    assert app.total_patient_negative == 0


def test_read_post_noborn_patient_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "IA": {
            "model_name": "LMW",
            "build_date": app.IA.build_date,
            "data_source": "data_sepsis 4.csv",
            "time_to_build": app.IA.time_to_build,
            "version": 0.1,
        },
        "API": {
            "average_preditction_response_time": round(
                round(app.time_to_predict.total_seconds() * 1000, 2)
                / (app.total_patient_negative + app.total_patient_positive),
                2,
            )
        },
        "prediction": {"total_positive": 1, "total_negative": 0, "total": 1},
    }


def test_post_negative_patient_test():
    response = client.post(
        "/predict/patient",
        json={
            "prg": 3,
            "pl": 88,
            "pr": 58,
            "sk": 11,
            "ts": 54,
            "m11": 24.8,
            "bd2": 0.267,
            "age": 22,
        },
    )

    assert response.status_code == 200
    assert response.text == '"Negative"'
    assert app.total_patient_positive == 1
    assert app.total_patient_negative == 1


def test_read_final_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "IA": {
            "model_name": "LMW",
            "build_date": app.IA.build_date,
            "data_source": "data_sepsis 4.csv",
            "time_to_build": app.IA.time_to_build,
            "version": 0.1,
        },
        "API": {
            "average_preditction_response_time": round(
                round(app.time_to_predict.total_seconds() * 1000, 2)
                / (app.total_patient_negative + app.total_patient_positive),
                2,
            )
        },
        "prediction": {"total_positive": 1, "total_negative": 1, "total": 2},
    }
