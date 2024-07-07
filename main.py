#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union

from fastapi import FastAPI, Form
from pydantic import BaseModel, PositiveInt
from datetime import datetime, timedelta

import LMW

IA = LMW.LMW()

total_patient_positive = total_patient_negative = 0
time_to_predict = timedelta()

app = FastAPI(openapi_url=None)


class Patient(BaseModel):
    prg: int
    pl: int
    pr: int
    sk: int
    ts: int
    m11: float
    bd2: float
    age: PositiveInt


@app.get("/health")
def get_health_status():
    if total_patient_negative + total_patient_positive == 0:
        return {
            "IA": {
                "model_name": IA.model_name,
                "build_date": IA.build_date,
                "data_source": IA.data_source,
                "time_to_build": IA.time_to_build,
                "version": IA.version,
            },
            "prediction": {
                "total_positive": total_patient_positive,
                "total_negative": total_patient_negative,
                "total": total_patient_negative + total_patient_positive,
            },
        }
    else:
        return {
            "IA": {
                "model_name": IA.model_name,
                "build_date": IA.build_date,
                "data_source": IA.data_source,
                "time_to_build": IA.time_to_build,
                "version": IA.version,
            },
            "API": {
                "average_preditction_response_time": round(
                    round(time_to_predict.total_seconds() * 1000, 2)
                    / (total_patient_negative + total_patient_positive),
                    2,
                )
            },
            "prediction": {
                "total_positive": total_patient_positive,
                "total_negative": total_patient_negative,
                "total": total_patient_negative + total_patient_positive,
            },
        }


@app.post("/predict/patient")
async def test_patient(patient: Patient):
    global total_patient_positive, total_patient_negative, time_to_predict

    start = datetime.now()

    if IA.run_model(patient):
        total_patient_positive += 1
        time_to_predict += datetime.now() - start
        return "Positive"
    else:
        total_patient_negative += 1
        time_to_predict += datetime.now() - start
        return "Negative"
