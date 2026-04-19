"""
robo_museo_aurora.py — El Robo del Museo Aurora

Durante la gala del Museo Aurora desapareció la “Máscara de Jade” de la sala central.
El guardia_nico estuvo registrado por el sistema de acceso en la puerta de seguridad (fuera de la sala)
durante el intervalo del robo. La restauradora_sara estaba fuera del museo (ticket verificado) esa noche.
La curadora_lucia tuvo acceso registrado a la sala central durante el intervalo del robo y no tiene coartada
verificada por un tercero. El asistente_diego declaró que lucia estuvo con él en el depósito toda la noche,
y lucia declaró lo mismo sobre diego. Además, registros internos indican que lucia tenía una deuda alta.

Como detective, concluí lo siguiente:
Una salida verificada o un registro de vigilancia objetivo constituyen coartada objetiva y descartan al sospechoso.
Tener acceso registrado a la sala durante el intervalo implica oportunidad (acceso_en_momento).
Tener deuda alta constituye motivo económico. Quien tenga motivo económico + acceso_en_momento + sin_coartada_verificada
es culpable. Quien da coartada a un culpable lo encubre. Si dos personas se dan coartada mutuamente, existe coartada cruzada.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, ForallGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    kb = KnowledgeBase()

    # --- Constantes ---
    curadora_lucia = Term("curadora_lucia")
    asistente_diego = Term("asistente_diego")
    guardia_nico = Term("guardia_nico")
    restauradora_sara = Term("restauradora_sara")

    sala_central = Term("sala_central")
    puerta_seguridad = Term("puerta_seguridad")

    # --- Hechos (>= 6) ---
    # Coartadas objetivas (descartan)
    kb.add_fact(Predicate("registro_vigilancia_objetivo", (guardia_nico, puerta_seguridad)))
    kb.add_fact(Predicate("ticket_salida_verificado", (restauradora_sara,)))

    # Oportunidad (acceso en momento del robo)
    kb.add_fact(Predicate("acceso_registrado", (curadora_lucia, sala_central)))

    # Motivo
    kb.add_fact(Predicate("deuda_alta", (curadora_lucia,)))

    # Coartadas cruzadas (mutuas)
    kb.add_fact(Predicate("da_coartada", (asistente_diego, curadora_lucia)))
    kb.add_fact(Predicate("da_coartada", (curadora_lucia, asistente_diego)))

    # Sin coartada verificada del culpable
    kb.add_fact(Predicate("sin_coartada_verificada", (curadora_lucia,)))

    # (Extra) Asistente no tiene coartada verificada (no lo vuelve culpable si no tiene acceso/motivo)
    kb.add_fact(Predicate("sin_coartada_verificada", (asistente_diego,)))

    # --- Variables ---
    X = Term("$X")
    Y = Term("$Y")
    L = Term("$L")

    # --- Reglas (>= 4) ---
    # 1) Coartada objetiva por vigilancia
    kb.add_rule(
        Rule(
            head=Predicate("coartada_objetiva", (X,)),
            body=(Predicate("registro_vigilancia_objetivo", (X, L)),),
        )
    )

    # 2) Coartada objetiva por ticket de salida
    kb.add_rule(
        Rule(
            head=Predicate("coartada_objetiva", (X,)),
            body=(Predicate("ticket_salida_verificado", (X,)),),
        )
    )

    # 3) Quien tiene coartada objetiva queda descartado
    kb.add_rule(
        Rule(
            head=Predicate("descartado", (X,)),
            body=(Predicate("coartada_objetiva", (X,)),),
        )
    )

    # 4) Acceso registrado implica acceso_en_momento (oportunidad)
    kb.add_rule(
        Rule(
            head=Predicate("acceso_en_momento", (X,)),
            body=(Predicate("acceso_registrado", (X, L)),),
        )
    )

    # 5) Deuda alta implica motivo_economico
    kb.add_rule(
        Rule(
            head=Predicate("motivo_economico", (X,)),
            body=(Predicate("deuda_alta", (X,)),),
        )
    )

    # 6) Culpable: motivo + acceso_en_momento + sin_coartada_verificada
    kb.add_rule(
        Rule(
            head=Predicate("culpable", (X,)),
            body=(
                Predicate("motivo_economico", (X,)),
                Predicate("acceso_en_momento", (X,)),
                Predicate("sin_coartada_verificada", (X,)),
            ),
        )
    )

    # 7) Encubridor: da coartada a un culpable
    kb.add_rule(
        Rule(
            head=Predicate("encubridor", (X,)),
            body=(Predicate("da_coartada", (X, Y)), Predicate("culpable", (Y,))),
        )
    )

    # 8) Coartada cruzada (mutua)
    kb.add_rule(
        Rule(
            head=Predicate("coartada_cruzada", (X, Y)),
            body=(Predicate("da_coartada", (X, Y)), Predicate("da_coartada", (Y, X))),
        )
    )

    return kb


CASE = CrimeCase(
    id="robo_museo_aurora",
    title="El Robo del Museo Aurora",
    suspects=("curadora_lucia", "asistente_diego", "guardia_nico", "restauradora_sara"),
    narrative=__doc__,
    description=(
        "Robo de una pieza en gala. Dos sospechosos quedan descartados por coartada objetiva; "
        "una sospechosa tiene motivo económico, oportunidad (acceso registrado) y falta de coartada verificada."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿Guardia Nico está descartado por coartada objetiva?",
            goal=Predicate("descartado", (Term("guardia_nico"),)),
        ),
        QuerySpec(
            description="¿Restauradora Sara está descartada por salida verificada?",
            goal=Predicate("descartado", (Term("restauradora_sara"),)),
        ),
        QuerySpec(
            description="¿Curadora Lucia es culpable?",
            goal=Predicate("culpable", (Term("curadora_lucia"),)),
        ),
        QuerySpec(
            description="¿Asistente Diego está encubriendo al culpable?",
            goal=Predicate("encubridor", (Term("asistente_diego"),)),
        ),
        # ExistsGoal (requisito): existe una coartada cruzada con Lucia
        QuerySpec(
            description="¿Existe coartada cruzada involucrando a Lucia?",
            goal=ExistsGoal(
                "$X",
                Predicate("coartada_cruzada", (Term("$X"), Term("curadora_lucia"))),
            ),
        ),
        # ForallGoal (extra): todo culpable tuvo acceso en el momento
        QuerySpec(
            description="¿Todo culpable tuvo acceso_en_momento?",
            goal=ForallGoal(
                "$X",
                Predicate("culpable", (Term("$X"),)),
                Predicate("acceso_en_momento", (Term("$X"),)),
            ),
        ),
    ),
)