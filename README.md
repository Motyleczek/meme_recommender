# meme_recommender
Semester project for advanced databases class

## 1. PostgreSQL installation

https://www.postgresql.org/download/

## 2. Python 3.X installation

https://www.python.org/downloads/

## 3. Make installation

Linux: apt / other package manager

Windows: https://gnuwin32.sourceforge.net/packages/make.htm

Mac: Brew

## 4. Requirements installation (pip)

`pip3 install -r requirements.txt`

## 5. Running

Before first run, copy `.env.example` to `.env` and fine-tune the settings to match your environment:

- fill in your PostgreSQL credentials (starting with `DB_`)
- generate a unique secret key (e.g. from https://www.uuidgenerator.net/) and save it as `APP_SECRET`

Run `make install` for the first time.

Additionally, for the first time you must create an empty database in PostgreSQL for the project - it's name must match the `DB_NAME` in `.env`. Run: `psql` (on Windows, you might want `psql -u postgres` and type in password `postgres` for a default installation) and type `create database <DB_NAME>`.

Then, run `make start`. Note: all commands starting with `make` must be run from the root catalogue of this project (the one in which `Makefile` resides in).