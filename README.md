# bowtie_home_assessment
Hello!
- To run server create venv and run `pip install -r requirements.txt` from root folder
- `python3 manage.py migrate`
- `python3 manage.py runserver`

Main endpoint: GET `http://127.0.0.1:8000/doctor/doctors/` (list of doctors)
- GET `http://127.0.0.1:8000/doctor/doctors/<id>` doctor detail
- GET `http://127.0.0.1:8000/doctor/doctors/?district=Central&expand=consultation_fee,address` filter by district

Other cases such as create Doctor, filtering can be found in `doctor.test.py`


1. Choice of Framework & Library: Django & DRF
- a) Benefits are extensive useful functionality ORM, migrations, serializers, REST framework, support of CRUD operations
    Drawbacks are monolithic structure, overkill for smaller projects.
- b) Ease of implementation and testing; The project can bes easily extended

2. Potential Improvement
- Add more filters like search by doctor's availability via schedules
- Add search, order by field name, e.g. name, category, address
- Create view for schedule for visualization and availability calendar

3. Production consideration
- Depending on whether API will be public or private create authorization and assign 
permission access for the view
- Change Django settings like DEBUG=False, set ALLOWED_HOSTS, SSL certificate setup, maybe docker container

4. Assumptions
- a) Each doctor object has separate schedule, fee so that by changing them it only affects one Doctor.
All API functionality included in one DRF viewset escape complexity. 5 models were created to split
data logically 
- b) ___
