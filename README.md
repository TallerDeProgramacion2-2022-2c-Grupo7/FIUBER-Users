# FIUBER-Users

FIUBER's Users service.

![licence](https://img.shields.io/github/license/TallerDeProgramacion2-2022-2c-Grupo7/FIUBER-Users)
[![Deploy](https://github.com/TallerDeProgramacion2-2022-2c-Grupo7/FIUBER-Users/actions/workflows/deployment.yml/badge.svg?branch=main)](https://github.com/TallerDeProgramacion2-2022-2c-Grupo7/FIUBER-Users/actions/workflows/deployment.yml)

This service was built using Python's web application framework [Fast API](https://fastapi.tiangolo.com/).

## Local installation & usage

Install dependencies. From within the root folder of the repository, run:
```shell
pip install -r requirements.txt
```

Copy your `firebase_credentials.json` file into the `src` folder of the repository, then run:
```shell
uvicorn main:app --reload --port 8000
```
