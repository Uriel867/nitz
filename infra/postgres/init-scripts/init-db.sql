-- TODO: Uriel to create relevant tables
-- TODO: create triggers and procedures


CREATE TABLE IF NOT EXISTS summoner_info (
    puuid TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    tag TEXT NOT NULL
);

-- Metadata table
CREATE TABLE match_metadata (
    match_id TEXT PRIMARY KEY,
    data_version TEXT,
    participants TEXT[] -- List of participant PUUIDs
);

-- Info table
CREATE TABLE match_info (
    match_id TEXT PRIMARY KEY REFERENCES metadata(match_id),
    end_of_game_result TEXT,
    game_creation BIGINT,
    game_duration BIGINT,
    game_end_timestamp BIGINT,
    game_id BIGINT,
    game_mode TEXT,
    game_name TEXT,
    game_start_timestamp BIGINT,
    game_type TEXT,
    game_version TEXT,
    map_id INTEGER,
    platform_id TEXT,
    queue_id INTEGER,
    tournament_code TEXT
);

-- Participant table (simplified; add more fields as needed)
CREATE TABLE participant (
    participant_id SERIAL PRIMARY KEY,
    match_id TEXT REFERENCES metadata(match_id),
    all_in_pings INTEGER,
    assist_me_pings INTEGER,
    assists INTEGER,
    baron_kills INTEGER,
    bounty_level INTEGER,
    champ_experience INTEGER,
    champ_level INTEGER,
    champion_id INTEGER, -- reference?
    champion_name TEXT,
    command_pings INTEGER,
    champion_transform INTEGER,
    consumables_purchased INTEGER,
    

);

-- Team table
CREATE TABLE match_team (
    team_id INTEGER,
    match_id TEXT REFERENCES metadata(match_id),
    win BOOLEAN,
    PRIMARY KEY (match_id, team_id)
);

-- Ban table
CREATE TABLE match_ban (
    team_id INTEGER,
    match_id TEXT REFERENCES metadata(match_id),
    champion_id INTEGER,
    pick_turn INTEGER,
    PRIMARY KEY (match_id, team_id, pick_turn)
);

-- Objectives table
CREATE TABLE match_objectives (
    match_id TEXT REFERENCES metadata(match_id),
    team_id INTEGER,
    objective_type TEXT,
    first BOOLEAN,
    kills INTEGER,
    PRIMARY KEY (match_id, team_id, objective_type)
);

CREATE TABLE match_objective (
    first BOOLEAN,
    kills INT
);

CREATE TABLE IF NOT EXISTS challenges (
    twelveAssistStreakCount INTEGER,
    baronBuffGoldAdvantageOverThreshold INTEGER,
    controlWardTimeCoverageInRiverOrEnemyHalf FLOAT,
    earliestBaron INTEGER,
    earliestDragonTakedown INTEGER,
    earliestElderDragon INTEGER,
    earlyLaningPhaseGoldExpAdvantage INTEGER,
    fasterSupportQuestCompletion INTEGER,
    fastestLegendary INTEGER,
    hadAfkTeammate INTEGER,
    highestChampionDamage INTEGER,
    highestCrowdControlScore INTEGER,
    highestWardKills INTEGER,
    junglerKillsEarlyJungle INTEGER,
    killsOnLanersEarlyJungleAsJungler INTEGER,
    laningPhaseGoldExpAdvantage INTEGER,
    legendaryCount INTEGER,
    maxCsAdvantageOnLaneOpponent FLOAT,
    maxLevelLeadLaneOpponent INTEGER,
    mostWardsDestroyedOneSweeper INTEGER,
    mythicItemUsed INTEGER,
    playedChampSelectPosition INTEGER,
    soloTurretsLategame INTEGER,
    takedownsFirst25Minutes INTEGER,
    teleportTakedowns INTEGER,
    thirdInhibitorDestroyedTime INTEGER,
    threeWardsOneSweeperCount INTEGER,
    visionScoreAdvantageLaneOpponent FLOAT,
    InfernalScalePickup INTEGER,
    fistBumpParticipation INTEGER,
    voidMonsterKill INTEGER,
    abilityUses INTEGER,
    acesBefore15Minutes INTEGER,
    alliedJungleMonsterKills FLOAT,
    baronTakedowns INTEGER,
    blastConeOppositeOpponentCount INTEGER,
    bountyGold INTEGER,
    buffsStolen INTEGER,
    completeSupportQuestInTime INTEGER,
    controlWardsPlaced INTEGER,
    damagePerMinute FLOAT,
    damageTakenOnTeamPercentage FLOAT,
    dancedWithRiftHerald INTEGER,
    deathsByEnemyChamps INTEGER,
    dodgeSkillShotsSmallWindow INTEGER,
    doubleAces INTEGER,
    dragonTakedowns INTEGER,
    legendaryItemUsed TEXT,  -- List[int] stored as comma-separated string
    effectiveHealAndShielding FLOAT,
    elderDragonKillsWithOpposingSoul INTEGER,
    elderDragonMultikills INTEGER,
    enemyChampionImmobilizations INTEGER,
    enemyJungleMonsterKills FLOAT,
    epicMonsterKillsNearEnemyJungler INTEGER,
    epicMonsterKillsWithin30SecondsOfSpawn INTEGER,
    epicMonsterSteals INTEGER,
    epicMonsterStolenWithoutSmite INTEGER,
    firstTurretKilled INTEGER,
    firstTurretKilledTime FLOAT,
    flawlessAces INTEGER,
    fullTeamTakedown INTEGER,
    gameLength FLOAT,
    getTakedownsInAllLanesEarlyJungleAsLaner INTEGER,
    goldPerMinute FLOAT,
    hadOpenNexus INTEGER,
    immobilizeAndKillWithAlly INTEGER,
    initialBuffCount INTEGER,
    initialCrabCount INTEGER,
    jungleCsBefore10Minutes FLOAT,
    junglerTakedownsNearDamagedEpicMonster INTEGER,
    kda FLOAT,
    killAfterHiddenWithAlly INTEGER,
    killedChampTookFullTeamDamageSurvived INTEGER,
    killingSprees INTEGER,
    killParticipation FLOAT,
    killsNearEnemyTurret INTEGER,
    killsOnOtherLanesEarlyJungleAsLaner INTEGER,
    killsOnRecentlyHealedByAramPack INTEGER,
    killsUnderOwnTurret INTEGER,
    killsWithHelpFromEpicMonster INTEGER,
    knockEnemyIntoTeamAndKill INTEGER,
    kTurretsDestroyedBeforePlatesFall INTEGER,
    landSkillShotsEarlyGame INTEGER,
    laneMinionsFirst10Minutes INTEGER,
    lostAnInhibitor INTEGER,
    maxKillDeficit INTEGER,
    mejaisFullStackInTime INTEGER,
    moreEnemyJungleThanOpponent FLOAT,
    multiKillOneSpell INTEGER,  -- Added description from user
    multikills INTEGER,
    multikillsAfterAggressiveFlash INTEGER,
    multiTurretRiftHeraldCount INTEGER,
    outerTurretExecutesBefore10Minutes INTEGER,
    outnumberedKills INTEGER,
    outnumberedNexusKill INTEGER,
    perfectDragonSoulsTaken INTEGER,
    perfectGame INTEGER,
    pickKillWithAlly INTEGER,
    poroExplosions INTEGER,
    quickCleanse INTEGER,
    quickFirstTurret INTEGER,
    quickSoloKills INTEGER,
    riftHeraldTakedowns INTEGER,
    saveAllyFromDeath INTEGER,
    scuttleCrabKills INTEGER,
    shortestTimeToAceFromFirstTakedown FLOAT,
    skillshotsDodged INTEGER,
    skillshotsHit INTEGER,
    snowballsHit INTEGER,
    soloBaronKills INTEGER,
    SWARM_DefeatAatrox INTEGER,
    SWARM_DefeatBriar INTEGER,
    SWARM_DefeatMiniBosses INTEGER,
    SWARM_EvolveWeapon INTEGER,
    SWARM_Have3Passives INTEGER,
    SWARM_KillEnemy INTEGER,
    SWARM_PickupGold FLOAT,
    SWARM_ReachLevel50 INTEGER,
    SWARM_Survive15Min INTEGER,
    SWARM_WinWith5EvolvedWeapons INTEGER,
    soloKills INTEGER,
    stealthWardsPlaced INTEGER,
    survivedSingleDigitHpCount INTEGER,
    survivedThreeImmobilizesInFight INTEGER,
    takedownOnFirstTurret INTEGER,
    takedowns INTEGER,
    takedownsAfterGainingLevelAdvantage INTEGER,
    takedownsBeforeJungleMinionSpawn INTEGER,
    takedownsFirstXMinutes INTEGER,
    takedownsInAlcove INTEGER,
    takedownsInEnemyFountain INTEGER,
    teamBaronKills INTEGER,
    teamDamagePercentage FLOAT,
    teamElderDragonKills INTEGER,
    teamRiftHeraldKills INTEGER,
    tookLargeDamageSurvived INTEGER,
    turretPlatesTaken INTEGER,
    turretsTakenWithRiftHerald INTEGER,
    turretTakedowns INTEGER,
    twentyMinionsIn3SecondsCount INTEGER,
    twoWardsOneSweeperCount INTEGER,
    unseenRecalls INTEGER,
    visionScorePerMinute FLOAT,
    wardsGuarded INTEGER,
    wardTakedowns INTEGER,
    wardTakedownsBefore20M INTEGER
);
