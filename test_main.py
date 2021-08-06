from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Data": "Please Check Docs for more information"}
    print('Test index')


def test_get_report():
    response = client.get("/company/reports/gb/1/?minyear=1&maxyear=1")
    assert response.status_code == 200
    assert response.json() == {
        "financials": [
            {
                "year": 1,
                "ebit": 1,
                "equity": 1,
                "sales": 1,
                "total_liabilities": 1,
                "company_id": "gb1",
                "retained_earnings": 1,
                "total_assets": 1
            }
        ]
    }
    print('Test get report')


def test_post_report():
    jj = {
        "year": 1999,
        "ebit": 1,
        "equity": 1,
        "retained_earnings": 1,
        "sales": 1,
        "total_assets": 1,
        "total_liabilities": 1
    }
    response = client.post("/company/reports/gb/1/", json=jj)
    assert response.status_code == 200
    assert response.json() == {
        "Data": "Commit successful"
    }


def test_zscores():
    data = {"financials": [
        {"year": 2020, "ebit": 123.45, "equity": 234.56, "retained_earnings": 345.67, "sales":
            1234.56, "total_assets": 345.67, "total_liabilities": 456.78},
        {"year": 2019, "ebit": 122.63, "equity": 224.56, "retained_earnings": 325.33, "sales":
            1214.99, "total_assets": 325.04, "total_liabilities": 426.78},
        {"year": 2018, "ebit": 120.17, "equity": 214.06, "retained_earnings": 225.00, "sales":
            1204.01, "total_assets": 305.11, "total_liabilities": 426.78},
        {"year": 2017, "ebit": 118.23, "equity": 204.96, "retained_earnings": 125.97, "sales":
            1200.00, "total_assets": 290.75, "total_liabilities": 426.78},
        {"year": 2016, "ebit": 116.05, "equity": 234.56, "retained_earnings": 105.11, "sales":
            1010.82, "total_assets": 250.13, "total_liabilities": 426.78}]}

    response = client.put("/company/gb/1", json=data)

    assert response.status_code == 200
    assert response.json() == {
        "scores": [
            {
                "year": 2020,
                "zscore": 6.07242023479448
            },
            {
                "year": 2019,
                "zscore": 6.324327195244421
            },
            {
                "year": 2018,
                "zscore": 6.100709234338317
            },
            {
                "year": 2017,
                "zscore": 5.80244252763309
            },
            {
                "year": 2016,
                "zscore": 5.642835608795672
            }
        ]
    }
    print('Test zscores')
