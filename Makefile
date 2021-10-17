


install-pkg:
	@pip install -r requirements.txt 

serve:
	@export FLASK_APP=run; flask run

