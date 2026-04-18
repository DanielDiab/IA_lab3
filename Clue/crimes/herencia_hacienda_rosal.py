"""
herencia_hacienda_rosal.py — La Herencia Maldita de Hacienda El Rosal

Don Evaristo fue hallado muerto con sedante disuelto en su medicación nocturna.
Don Evaristo había anunciado esa tarde que cambiaría su testamento al día siguiente.
La Enfermera Campos tiene coartada verificada por la cámara de la enfermería.
El Abogado Restrepo hereda con el testamento actual y quedaría excluido si el testamento cambiara.
El Sobrino Esteban hereda con el testamento actual y también quedaría excluido si el testamento cambiara.
La Secretaria Luna no hereda con el testamento actual, pero sí lo haría con el nuevo.
Las huellas del Sobrino Esteban aparecen en el vaso de medicación adulterada.
El vaso con medicación adulterada es el objeto del crimen.
El Abogado Restrepo, el Sobrino Esteban y la Secretaria Luna no tienen coartada verificada.
El Sobrino Esteban acusa a la Secretaria Luna.
El Abogado Restrepo acusa al Sobrino Esteban.
La Secretaria Luna declara que el Sobrino Esteban estuvo con ella esa noche.

Como detective, he llegado a las siguientes conclusiones:
Quien tiene coartada verificada por medios objetivos queda descartado.
Quien hereda actualmente y perdería con el cambio de testamento tiene motivo doble para evitar ese cambio.
Quien tiene huellas en el objeto del crimen tiene evidencia física en su contra.
Quien tiene motivo doble, sin coartada y con evidencia física en su contra es culpable.
Cuando el culpable acusa a otra persona para desviar la investigación, esa acusación es un desvío sospechoso.
Quien da coartada al culpable está encubriendo el crimen.
Una acusación es corroborada cuando el acusador también tiene motivo doble y el acusado tiene evidencia física.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    enfermera_campos  = Term("enfermera_campos")
    abogado_restrepo  = Term("abogado_restrepo")
    sobrino_esteban   = Term("sobrino_esteban")
    secretaria_luna   = Term("secretaria_luna")
    vaso_adulterado   = Term("vaso_adulterado")

    # --- Hechos ---
    # Enfermera Campos tiene coartada verificada objetivamente (cámara de enfermería)
    kb.add_fact(Predicate("coartada_objetiva", (enfermera_campos,)))
    # Abogado Restrepo hereda con testamento actual
    kb.add_fact(Predicate("hereda_actual", (abogado_restrepo,)))
    # Abogado Restrepo perdería con el cambio de testamento
    kb.add_fact(Predicate("perderia_con_cambio", (abogado_restrepo,)))
    # Sobrino Esteban hereda con testamento actual
    kb.add_fact(Predicate("hereda_actual", (sobrino_esteban,)))
    # Sobrino Esteban perdería con el cambio de testamento
    kb.add_fact(Predicate("perderia_con_cambio", (sobrino_esteban,)))
    # Las huellas del Sobrino Esteban están en el vaso de medicación adulterada
    kb.add_fact(Predicate("huellas_en", (sobrino_esteban, vaso_adulterado)))
    # El vaso adulterado es el objeto del crimen
    kb.add_fact(Predicate("objeto_crimen", (vaso_adulterado,)))
    # Abogado Restrepo no tiene coartada verificada
    kb.add_fact(Predicate("sin_coartada", (abogado_restrepo,)))
    # Sobrino Esteban no tiene coartada verificada
    kb.add_fact(Predicate("sin_coartada", (sobrino_esteban,)))
    # Secretaria Luna no tiene coartada verificada
    kb.add_fact(Predicate("sin_coartada", (secretaria_luna,)))
    # Sobrino Esteban acusa a Secretaria Luna
    kb.add_fact(Predicate("acusa", (sobrino_esteban, secretaria_luna)))
    # Abogado Restrepo acusa al Sobrino Esteban
    kb.add_fact(Predicate("acusa", (abogado_restrepo, sobrino_esteban)))
    # Secretaria Luna da coartada al Sobrino Esteban
    kb.add_fact(Predicate("da_coartada", (secretaria_luna, sobrino_esteban)))

    # --- Reglas ---
    X = Term("$X")
    Y = Term("$Y")
    O = Term("$O")

    # Quien tiene coartada verificada por medios objetivos queda descartado
    kb.add_rule(Rule(
        head=Predicate("descartado", (X,)),
        body=(Predicate("coartada_objetiva", (X,)),),
    ))

    # Quien hereda actualmente y perdería con el cambio de testamento tiene motivo doble
    kb.add_rule(Rule(
        head=Predicate("motivo_doble", (X,)),
        body=(
            Predicate("hereda_actual", (X,)),
            Predicate("perderia_con_cambio", (X,)),
        ),
    ))

    # Quien tiene huellas en el objeto del crimen tiene evidencia física en su contra
    kb.add_rule(Rule(
        head=Predicate("evidencia_fisica", (X,)),
        body=(
            Predicate("huellas_en", (X, O)),
            Predicate("objeto_crimen", (O,)),
        ),
    ))

    # Quien tiene motivo doble, sin coartada y con evidencia física en su contra es culpable
    kb.add_rule(Rule(
        head=Predicate("culpable", (X,)),
        body=(
            Predicate("motivo_doble", (X,)),
            Predicate("sin_coartada", (X,)),
            Predicate("evidencia_fisica", (X,)),
        ),
    ))

    # Cuando el culpable acusa a otra persona para desviar la investigación, es un desvío sospechoso
    kb.add_rule(Rule(
        head=Predicate("desvio_sospechoso", (X, Y)),
        body=(
            Predicate("culpable", (X,)),
            Predicate("acusa", (X, Y)),
        ),
    ))

    # Quien da coartada al culpable está encubriendo el crimen
    kb.add_rule(Rule(
        head=Predicate("encubridor", (X,)),
        body=(
            Predicate("da_coartada", (X, Y)),
            Predicate("culpable", (Y,)),
        ),
    ))

    # Una acusación es corroborada cuando el acusador tiene motivo doble y el acusado tiene evidencia física
    kb.add_rule(Rule(
        head=Predicate("acusacion_corroborada", (X, Y)),
        body=(
            Predicate("acusa", (X, Y)),
            Predicate("motivo_doble", (X,)),
            Predicate("evidencia_fisica", (Y,)),
        ),
    ))

    return kb


CASE = CrimeCase(
    id="herencia_hacienda_rosal",
    title="La Herencia Maldita de Hacienda El Rosal",
    suspects=("enfermera_campos", "abogado_restrepo", "sobrino_esteban", "secretaria_luna"),
    narrative=__doc__,
    description=(
        "Un patriarca murió envenenado horas antes de cambiar su testamento. "
        "Dos herederos pierden con el cambio. Uno de ellos tiene las huellas en el vaso adulterado, "
        "acusa a quien gana con el nuevo testamento, y es encubierto por esa misma persona."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿La enfermera Campos está descartada?",
            goal=Predicate("descartado", (Term("enfermera_campos"),)),
        ),
        QuerySpec(
            description="¿El sobrino Esteban tiene motivo doble?",
            goal=Predicate("motivo_doble", (Term("sobrino_esteban"),)),
        ),
        QuerySpec(
            description="¿El sobrino Esteban es culpable?",
            goal=Predicate("culpable", (Term("sobrino_esteban"),)),
        ),
        QuerySpec(
            description="¿El sobrino Esteban hace un desvío sospechoso al acusar a Luna?",
            goal=Predicate("desvio_sospechoso", (Term("sobrino_esteban"), Term("secretaria_luna"))),
        ),
        QuerySpec(
            description="¿La acusación del Abogado Restrepo contra el sobrino está corroborada?",
            goal=Predicate("acusacion_corroborada", (Term("abogado_restrepo"), Term("sobrino_esteban"))),
        ),
    ),
)
