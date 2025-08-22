from tests.utils import sort_list_by_date, sort_list_by_activity, create_dummy_user_token

def test_get_applications(client, auth_header):
    """
    Returns a list of all applications associated with a user.
    """
    response = client.get("api/users/1/applications", headers=auth_header)

    assert response.status_code == 200

    applications = response.json["applications"]
    assert len(applications) == 4

    for application in applications:
        assert isinstance(application["application_id"], int)
        assert len(application["company"]) > 0
        assert len(application["position"]) > 0
        assert len(application["date_created"]) > 0
        assert application["status"] in ["Application sent", "In review", "Rejected", "Archived", "Offer received", "Offer accepted", "Offer declined"]
        assert all(key in application.keys() for key in ["job_url", "latest_event"]) 

def test_get_applications_nonexistent_id(client, auth_header):
    """
    Responds with 404 error if no user found with the given id
    """
    response = client.get("api/users/100/applications", headers=auth_header)

    assert response.status_code == 404
    assert response.json["message"] == "Resource not found"

def test_get_applications_invalid_id(client, auth_header):
    """
    Responds with 400 error if the given id is not valid
    """
    response = client.get("api/users/abc/applications", headers=auth_header)

    assert response.status_code == 404
    assert response.json["message"] == "Requested URL does not exist"

def test_get_applications_new_user(client):
    """
    Responds with an empty list if a user does not have any applications
    """
    response = client.get("api/users/4/applications", headers=create_dummy_user_token(4))

    assert response.status_code == 200
    assert len(response.json["applications"]) == 0


def test_get_applications_sorting_date_created(client, auth_header):
    """
    Applications can be sorted by date created
    """
    response = client.get("api/users/1/applications", headers=auth_header)
    applications = response.json["applications"]
    sorted_list = sorted(applications, key=sort_list_by_date, reverse=True)
    assert sorted_list == applications, "By default, applications must be sorted by date created in descending order"

    response = client.get("api/users/1/applications?order=asc", headers=auth_header)
    applications = response.json["applications"]
    sorted_list = sorted(applications, key=sort_list_by_date)
    assert sorted_list == applications, "Applications must be sorted by date created in ascending order"

    response = client.get("api/users/1/applications?order=desc", headers=auth_header)
    applications = response.json["applications"]
    sorted_list = sorted(applications, key=sort_list_by_date, reverse=True)
    assert sorted_list == applications, "Applications must be sorted by date created in descending order"

    response = client.get("api/users/1/applications?sort_by=date_created", headers=auth_header)
    applications = response.json["applications"]
    sorted_list = sorted(applications, key=sort_list_by_date, reverse=True)
    assert sorted_list == applications, "Applications must be sorted by date created in descending order"

    response = client.get("api/users/1/applications?sort_by=date_created&order=desc", headers=auth_header)
    applications = response.json["applications"]
    sorted_list = sorted(applications, key=sort_list_by_date, reverse=True)
    assert sorted_list == applications, "Applications must be sorted by date created in descending order"

    response = client.get("api/users/1/applications?sort_by=date_created&order=asc", headers=auth_header)
    applications = response.json["applications"]
    sorted_list = sorted(applications, key=sort_list_by_date)
    assert sorted_list == applications, "Applications must be sorted by date created in ascending order"

def test_get_applications_sorting_latest_event(client, auth_header):
    """
    Applications can be sorted by latest event
    """
    response = client.get("api/users/1/applications?sort_by=recent_activity", headers=auth_header)
    applications = response.json["applications"]
    sorted_list = sorted(applications, key=sort_list_by_activity, reverse=True)
    assert sorted_list == applications, "Applications must be sorted by latest event in descending order"

    response = client.get("api/users/1/applications?sort_by=recent_activity&order=desc", headers=auth_header)
    applications = response.json["applications"]
    sorted_list = sorted(applications, key=sort_list_by_activity, reverse=True)
    assert sorted_list == applications, "Applications must be sorted by latest event in descending order"

    response = client.get("api/users/1/applications?sort_by=recent_activity&order=asc", headers=auth_header)
    applications = response.json["applications"]
    sorted_list = sorted(applications, key=sort_list_by_activity)
    assert sorted_list == applications, "Applications must be sorted by latest event in ascending order"

def test_get_applications_invalid_sort(client, auth_header):
    """
    If sorting parameters are invalid, sorts by date created in descending order
    """
    response = client.get("api/users/1/applications?order=abc", headers=auth_header)
    applications = response.json["applications"]
    sorted_list = sorted(applications, key=sort_list_by_activity, reverse=True)
    assert sorted_list == applications

    response = client.get("api/users/1/applications?order=abc&sort_by=abc", headers=auth_header)
    applications = response.json["applications"]
    sorted_list = sorted(applications, key=sort_list_by_activity, reverse=True)
    assert sorted_list == applications

    response = client.get("api/users/1/applications?sort_by=abc", headers=auth_header)
    applications = response.json["applications"]
    sorted_list = sorted(applications, key=sort_list_by_activity, reverse=True)
    assert sorted_list == applications

def test_get_application_filter_by_status(client, auth_header):
    """
    Applications can be filtered by status: active (Application sent, In review, Offer received), rejected or archived (Archived, Offer accepted, Offer declined)
    """

    response = client.get("api/users/1/applications?status=active", headers=auth_header)
    applications = response.json["applications"]
    assert all(application["status"] in ["Application sent", "In review", "Offer received"] for application in applications)

    response = client.get("api/users/1/applications?status=rejected", headers=auth_header)
    applications = response.json["applications"]
    assert all(application["status"] == "Rejected" for application in applications)

    response = client.get("api/users/1/applications?status=archived", headers=auth_header)
    applications = response.json["applications"]
    assert all(application["status"] in  ["Archived", "Offer accepted", "Offer declined"] for application in applications)

def test_get_application_filter_by_invalid_status(client, auth_header):
    """
    Responds with a 400 error if the provided status is not valid
    """

    response = client.get("api/users/1/applications?status=abc", headers=auth_header)
    assert response.status_code == 400
    assert response.json["message"] == "Bad Request"
   
def test_get_applications_search(client, auth_header):
    """
    Supports search by company name or position
    """
    response = client.get("api/users/1/applications?search=open", headers=auth_header)
    applications = response.json["applications"]
    assert len(applications) > 0
    assert all("open" in application["company"].lower() or "open" in application["position"].lower() for application in applications)
    
    response = client.get("api/users/1/applications?search=eng", headers=auth_header)
    applications = response.json["applications"]
    assert len(applications) > 0
    assert all("eng" in application["company"].lower() or "eng" in application["position"].lower() for application in applications)

    response = client.get("api/users/1/applications?search=nonexistent", headers=auth_header)
    applications = response.json["applications"]
    assert len(applications) == 0