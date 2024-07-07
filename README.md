# LMW

## Introduction
Se repo stocke le code utilisé pour exécuter et construire le model LMW.

## LMW
LMW signifi LinuxMacWindows.

Se model permet de prédire si une personnes à le Syndrome d'infection générale et grave de l'organisme par des germes pathogènes (SEPSIS)

Le développement et le maintien en condition opérationnel est réaliser par l'équipe 1 de la R&d de Medos : 
Prénom NOM | Role 
 --- | ---
Antoine BERNARD | Chef de projet
Ludovic MARION | Développeur
Romain FALLURET | Développeur
Elie Yvon BOTOUKOU ONGOUYA | Responsable produit

## Utilisation du serveur de production
L'API est disponible en ligne sur 

Elle est hébergé par un EC2 sur AWS - Paris (EU-WEST-3).

## Fonctionnement local
Requiert [Python 3.12](https://www.python.org/ftp/python/3.12.4/)

**Exemple sous un système Linux :**

1 - Cloner le repo : 
```shell
git clone https://github.com/MedosR-D/Sepsis-IA.git
```

2 - Créer un environement local : 
```shell
python -m venv ./venv
```

3 - Entrer dans l'environement : 
```shell
source ./venv/bin/activate
```

4 - Installer les dépendances : 
```shell
pip install -r requirements.txt
```

5 - Lancement du code : 
```shell
fastapi dev main.py
```