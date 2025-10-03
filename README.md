# nitz

nitz is an application designed to help League of Legends (LoL) players to understand their current match state in real time.

Initially, the project started with Overwatch 2, but since Blizzard don't share match data, unfortunately, we decided to move forward with other candidates.

We are two Computer Science students who like gaming, math and code. 

Our goal is to give real time insights to players using Maching Learning (ML) and statistical analyses during their matches. This allows for better decision makings during games, and hopefully, better results.

Our course of actions is as follows:

- Get the backend working. Creating an API to fetch and store match data for later use (for developing the ML models). This includes developing the API, scheduling ETL processes and getting the databases up and running.
- After that, we'll be working on the ML and statistical models.
- In parallel, we'll be developing the frontend for users to be able to use the application.
- Lastly, hosting the backend on the cloud.

As for the architecture of the application, we've separated it into 2 main flows:

1. Inference
```mermaid
sequenceDiagram
    actor Client
    participant FastAPI
    participant Redis
    participant PostgreSQL
    participant RiotAPI
    participant PredictionService
    participant ModelRegistry
    
    Client ->> FastAPI: (1) Request prediction
    FastAPI ->> Redis: (2.1.1) Check if match data exists in cache
    Redis ->> FastAPI: (2.1.2) Get match data from cache
    FastAPI ->> PostgreSQL: (2.2.1) Request match data
    PostgreSQL ->> FastAPI: (2.2.2) Get match data
    PostgreSQL ->> Redis: (2.2.3) Cache data
    FastAPI ->> RiotAPI: (2.3.1) Request match data
    RiotAPI ->> FastAPI: (2.3.2) Get match data
    FastAPI ->> PostgreSQL: (2.3.3) Report data
    PostgreSQL ->> Redis: (2.3.4) Cache data
    FastAPI ->> PredictionService: (3) Request prediction
    PredictionService ->> PredictionService: (3.1) preprocessing
    PredictionService ->> ModelRegistry: (3.2) Request best model
    ModelRegistry ->> PredictionService: (3.3) Get best model
    PredictionService ->> PredictionService: (3.4) Predict
    PredictionService ->> PostgreSQL: (3.5) Report prediction
    PredictionService ->> FastAPI: (4) Get prediction
    FastAPI ->> Client: (5) Display prediction
    
    
```

2. Data gathering and ETL processes.

```mermaid
---
title: ETL from MongoDB to PostgreSQL
---
flowchart LR
    api[FastAPI]
    riotAPI[Riot Games API]
    dataPipeline[Airflow]
    mongodb[(MongoDB)]
    postgres[(PostgreSQL)]
    
    dataPipeline <-->|fetch existing data| api <-->|fetch existing data| mongodb
    dataPipeline -->|transform and load| postgres
    api <-->|fetch additional data| riotAPI
```
