from flask import Flask, render_template, redirect, flash, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask (__name__)
app.config ['SECRET_KEY'] = 'secret'

app.config ['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config ['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

# ##############################################################################

@app.route("/")
def homepage():
    """list the pets"""
    pets = Pet.query.all()
    return render_template ("home.html", pets= pets)

@app.route ("/add", methods = ["GET", "POST"])
def add_pet():
    """Add a pet."""
    form = AddPetForm()
    if form.validate_on_submit():
        data = {key: value for key, value in form.data.items()
                if key != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add (new_pet)
        db.session.commit()
        flash (f"{new_pet.name} added.")
        return redirect ("/")
    else:
        """Get route. Display the form"""
        return render_template ("add_pet_form.html", form = form)

@app.route ("/<int:pet_id>", methods = ["GET", "POST"])
def edit_pet(pet_id):
    """Edit pet"""

    # get pet info first
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm()

    if form.validate_on_submit():
        if (form.photo_url.data):
            pet.photo_url = form.photo_url.data
        if (form.age.data):
            pet.age = form.age.data
        if (form.notes.data):
            pet.notes = form.notes.data
        
        pet.available = form.available.data
   

        db.session.commit()

        flash(f"{pet.name} updated.")

        return redirect("/")

    else:
        """Dispaly the pet info and edit form"""
        return render_template ("edit_pet_form.html", pet =pet, form = form)


@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    """Return basic info about pet in JSON."""

    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, 
            "species": pet.species,
            "age": pet.age,
            "notes": pet.notes}

    return jsonify(info)

