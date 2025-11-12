from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddItemForm(FlaskForm):
    name = StringField('Nome do item', validators=[DataRequired()])
    submit = SubmitField('Add Item')
