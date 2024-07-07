#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, joblib
from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


class LMW:

    def __init__(self, date_source="data_sepsis 4.csv"):
        self.data_source = date_source

        start = datetime.now()
        self.build_model()
        self.time_to_build = round((datetime.now() - start).total_seconds() * 1000, 2)
        self.save_model()
        self.model_name = "LMW"
        self.version = 0.1

    def build_model(self):
        # On charge le fichier source dans un DataFrame
        df = pd.read_csv(self.data_source)

        # Suppression des colonnes non pertinentes
        df.drop(["ID", "Insurance"], axis=1, inplace=True)

        # Conversion de la colonne 'Sepssis' en booléen
        df["Sepssis"] = df["Sepssis"].apply(lambda row: row == "Positive")

        # Division du DataFrame en 90% d'entraînement et 10% de test
        df_train, df_test = train_test_split(df, test_size=0.10, random_state=42)

        # Séparation des caractéristiques et de la cible pour l'ensemble d'entraînement
        X_train_full = df_train.drop("Sepssis", axis=1)
        y_train_full = df_train["Sepssis"]

        # Séparation des données d'entraînement et de validation
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_full, y_train_full, test_size=0.25, random_state=42
        )

        # Normaliser les caractéristiques
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(df_test.drop("Sepssis", axis=1))
        # Création et entraînement du modèle de régression logistique
        self.model = LogisticRegression(max_iter=1000).fit(X_train_scaled, y_train)

        self.build_date = datetime.now().strftime("%b-%d-%Y %H:%M:%S")

        # Évaluation du modèle sur l'ensemble de validation
        print(
            "Accuracy on validation set:",
            round(self.model.score(X_val_scaled, y_val) * 100, 2),
            "%",
        )

        # Calcul de l'accuracy sur le DataFrame de test
        print(
            "Accuracy on test set:",
            round(
                accuracy_score(df_test["Sepssis"], self.model.predict(X_test_scaled))
                * 100,
                2,
            ),
            "%",
        )

    def save_model(self, modelName="LMW"):
        joblib.dump(self.model, os.path.abspath(modelName + ".joblib"))

    def load_model(self, model_name="LMW"):
        self.model_name = model_name
        self.model = joblib.load(model_name + ".joblib")

    def run_model(self, patient):
        return self.model.predict(
            self.scaler.transform(
                pd.DataFrame(
                    {
                        "PRG": patient.prg,
                        "PL": patient.pl,
                        "PR": patient.pr,
                        "SK": patient.sk,
                        "TS": patient.ts,
                        "M11": patient.m11,
                        "BD2": patient.bd2,
                        "Age": patient.age,
                    },
                    index=["1"],
                )
            )
        )
