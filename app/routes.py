from flask import Blueprint, render_template, redirect, jsonify
import urllib.parse as parse
import re
from sqlalchemy import func
from .models import Proyectos, Categorias, Proyectos_Categorias, Historico_clicks

bp = Blueprint('main', __name__)

# Funcion para volver diccionario
def to_dict(objs):
    result = []
    for obj in objs:
        dict_obj = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        result.append(dict_obj)
    return result

# URL Routing - Home Page
@bp.route("/")
def index():
    return render_template('index.html', 
                            projects=Proyectos.query.order_by(Proyectos.fecha.desc()).all(),
                            categorias=Categorias.query.all(),
                            categorias1=Categorias.query.all())

@bp.route("/<path:path>/")
def page(path):
    if Proyectos.query.with_entities(Proyectos.path).\
        distinct().filter(Proyectos.path == path).first() is not None: 
        Historico_clicks.insert(
            id_proyecto=Proyectos.query.with_entities(Proyectos.id).distinct().filter(Proyectos.path == path).first()[0])
        return render_template(path)
    elif re.search(r"\w*/index.html", path):
        return redirect('/')
    elif re.search(r'categoria=\w+', path):
        categoria = parse.unquote(path).split('=')[-1]
        if categoria == 'ALL':
            projects = Proyectos.query.with_entities(Proyectos,\
                                            func.strftime('%Y-%m-%d', Proyectos.fecha).\
                                                label('formatted_date')).\
                                                    order_by(Proyectos.fecha.desc()).all()
            return [{**to_dict([proj])[0], 'fecha': formatted_date} for proj, formatted_date in projects]
        elif Categorias.query.with_entities(Categorias.nombre).\
            distinct().filter(Categorias.nombre == categoria).first() is not None:
            proj_fil = Proyectos.query.\
                            join(Proyectos_Categorias, Proyectos.id == Proyectos_Categorias.id_proyecto).\
                            join(Categorias, Proyectos_Categorias.id_categoria == Categorias.id).\
                                filter(Categorias.nombre == categoria).\
                                with_entities(Proyectos,\
                                            func.strftime('%Y-%m-%d', Proyectos.fecha).\
                                                label('formatted_date')).\
                                                    order_by(Proyectos.fecha.desc()).all()
            return jsonify([{**to_dict([proj])[0], 'fecha': formatted_date} for proj, formatted_date in proj_fil])
        else:
            return render_template('404.html')
    else:
        return render_template('404.html')