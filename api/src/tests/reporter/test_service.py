from unittest.mock import MagicMock
from reporter.service import LoLStatsService


def make_mongo_client(summoners_collection_mock, matches_collection_mock=None):
    mongo_client = MagicMock()
    db = MagicMock()
    db.summoners = summoners_collection_mock
    db.matches = matches_collection_mock or MagicMock()
    mongo_client.lol = db
    return mongo_client


def test_insert_summoner_success():
    # Arrange
    inserted_id = "507f1f77bcf86cd799439011"
    insert_result = MagicMock()
    insert_result.inserted_id = inserted_id

    summoners_collection = MagicMock()
    summoners_collection.insert_one.return_value = insert_result

    client = make_mongo_client(summoners_collection)
    svc = LoLStatsService(client)

    # Act
    res = svc.insert_summoner("playerName", "TAG")

    # Assert
    assert isinstance(res, dict)
    assert res.get("success") is True
    assert "Inserted document with ID" in res.get("message", "")
    assert inserted_id in res["message"]


def test_insert_summoner_exception():
    # Arrange
    summoners_collection = MagicMock()
    summoners_collection.insert_one.side_effect = Exception("boom")

    client = make_mongo_client(summoners_collection)
    svc = LoLStatsService(client)

    # Act
    res = svc.insert_summoner("playerName", "TAG")

    # Assert
    assert isinstance(res, dict)
    assert res.get("success") is False
    assert "An error occurred while inserting data" in res.get("error", "")
    assert "boom" in res.get("error", "")


def test_insert_many_summoners_success():
    # Arrange
    inserted_ids = ["id1", "id2", "id3"]
    insert_result = MagicMock()
    insert_result.inserted_ids = inserted_ids

    summoners_collection = MagicMock()
    summoners_collection.insert_many.return_value = insert_result

    client = make_mongo_client(summoners_collection)
    svc = LoLStatsService(client)
    summoners_list = [{"game_name": "a", "tag_line": "A"}, {"game_name": "b", "tag_line": "B"},
                      {"game_name": "c", "tag_line": "C"}]

    # Act
    res = svc.insert_many_summoners(summoners_list)

    # Assert
    assert isinstance(res, dict)
    assert res.get("success") is True
    assert f"Inserted {len(inserted_ids)} documents" in res.get("message", "")
    summoners_collection.insert_many.assert_called_once_with(summoners_list)


def test_insert_many_summoners_exception():
    # Arrange
    summoners_collection = MagicMock()
    summoners_collection.insert_many.side_effect = Exception("boom")

    client = make_mongo_client(summoners_collection)
    svc = LoLStatsService(client)

    # Act
    res = svc.insert_many_summoners([{"game_name": "x", "tag_line": "X"}])

    # Assert
    assert isinstance(res, dict)
    assert res.get("success") is False
    assert "An error occurred while inserting data" in res.get("error", "")
    assert "boom" in res.get("error", "")


def test_get_all_summoners_empty():
    # Arrange
    summoners_collection = MagicMock()
    summoners_collection.find.return_value = []
    client = make_mongo_client(summoners_collection)
    svc = LoLStatsService(client)

    # Act
    res = svc.get_all_summoners()

    # Assert
    assert isinstance(res, dict)
    assert res.get("success") is True
    assert "No summoners found" in res.get("message", "")


def test_get_all_summoners_success():
    # Arrange
    expected = [{"game_name": "a", "tag_line": "A"}, {"game_name": "b", "tag_line": "B"}]
    summoners_collection = MagicMock()
    summoners_collection.find.return_value = expected
    client = make_mongo_client(summoners_collection)
    svc = LoLStatsService(client)

    # Act
    res = svc.get_all_summoners()

    # Assert
    assert isinstance(res, list)
    assert res == expected


def test_get_all_summoners_exception():
    # Arrange
    summoners_collection = MagicMock()
    summoners_collection.find.side_effect = Exception("boom")
    client = make_mongo_client(summoners_collection)
    svc = LoLStatsService(client)

    # Act
    res = svc.get_all_summoners()

    # Assert
    assert isinstance(res, dict)
    assert res.get("success") is False
    assert "An error occurred while fetching summoners" in res.get("error", "")
    assert "boom" in res.get("error", "")


def test_get_match_data_by_id_found():
    # Arrange
    match_doc = {"match_id": "m1", "match_data": {"score": 42}}
    matches_collection = MagicMock()
    matches_collection.find_one.return_value = match_doc
    client = make_mongo_client(MagicMock(), matches_collection)
    svc = LoLStatsService(client)

    # Act
    res = svc.get_match_data_by_id("m1")

    # Assert
    assert isinstance(res, dict)
    assert res.get("match_id") == "m1"
    assert res.get("match_data") == {"score": 42}


def test_get_match_data_by_id_not_found():
    # Arrange
    matches_collection = MagicMock()
    matches_collection.find_one.return_value = None
    client = make_mongo_client(MagicMock(), matches_collection)
    svc = LoLStatsService(client)

    # Act
    res = svc.get_match_data_by_id("m2")

    # Assert
    assert isinstance(res, dict)
    assert res.get("success") is True
    assert "match data not found" in res.get("message", "")


def test_get_match_data_by_id_exception():
    # Arrange
    matches_collection = MagicMock()
    matches_collection.find_one.side_effect = Exception("boom")
    client = make_mongo_client(MagicMock(), matches_collection)
    svc = LoLStatsService(client)

    # Act
    res = svc.get_match_data_by_id("m3")

    # Assert
    assert isinstance(res, dict)
    assert res.get("success") is False
    assert "An error occurred while fetching match data" in res.get("error", "")
    assert "boom" in res.get("error", "")


def test_insert_match_data_by_id_success():
    # Arrange
    inserted_id = "507f1f77bcf86cd799439011"
    insert_result = MagicMock()
    insert_result.inserted_id = inserted_id

    matches_collection = MagicMock()
    matches_collection.insert_one.return_value = insert_result

    client = make_mongo_client(MagicMock(), matches_collection)
    svc = LoLStatsService(client)

    # Act
    res = svc.insert_match_data_by_id("m1", {"score": 100})

    # Assert
    assert isinstance(res, dict)
    assert res.get("success") is True
    assert "Inserted match data with ID" in res.get("message", "")
    assert inserted_id in res["message"]
    matches_collection.insert_one.assert_called_once_with({"match_id": "m1", "match_data": {"score": 100}})


def test_insert_match_data_by_id_exception():
    # Arrange
    matches_collection = MagicMock()
    matches_collection.insert_one.side_effect = Exception("boom")

    client = make_mongo_client(MagicMock(), matches_collection)
    svc = LoLStatsService(client)

    # Act
    res = svc.insert_match_data_by_id("m1", {"score": 0})

    # Assert
    assert isinstance(res, dict)
    assert res.get("success") is False
    assert "An error occurred while inserting match data" in res.get("error", "")
    assert "boom" in res.get("error", "")
