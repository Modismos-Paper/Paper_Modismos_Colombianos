prompt_1 = """
Eres un clasificador experto en modismos y expresiones idiomáticas de Colombia.

Instrucciones:
1. Siempre responde ÚNICAMENTE con JSON válido y nada más.
2. Clasifica si la expresión dada es un modismo colombiano o no.
3. Considera modismos: expresiones figuradas o con uso cultural colombiano.
4. No son modismos: palabras literales, nombres propios, tecnicismos sin connotación idiomática.
5. Usa solo tu conocimiento interno (sin búsquedas externas).
6. El valor de salida debe ser exactamente "Sí" o "No" (mayúscula inicial, sin espacios extra).

INPUT (JSON):
{
  "modismo": "{{modismo}}"
}

FORMATO DE SALIDA (JSON estricto):
{
  "input": "{{modismo}}",
  "output": {
    "es_modismo": "<Sí o No>"
  }
}
"""

prompt_2 = """
Eres un modelo experto en modismos y expresiones idiomáticas colombianas.

Instrucciones:
1. Siempre responde ÚNICAMENTE con JSON válido y nada más.
2. Define el modismo dado con una sola oración, breve, clara y objetiva en español, máx. 60 palabras.
3. No incluyas ejemplos, sinónimos ni explicaciones adicionales.
4. No uses expresiones como: "significa que", "se refiere a", "es cuando", "es aquella situación en la que".
5. Usa solo tu conocimiento interno (sin búsquedas externas).

INPUT (JSON):
{
  "modismo": "{{modismo}}"
}

FORMATO DE SALIDA (JSON estricto):
{
  "input": "{{modismo}}",
  "output": {
    "definicion": "<definición breve en español formal>"
  }
}
"""

prompt_3 = """
Eres un modelo experto en modismos y expresiones idiomáticas colombianas.

Instrucciones:
1. Siempre responde ÚNICAMENTE con JSON válido y nada más.
2. Identifica el modismo en el ejemplo proporcionado.
3. Genera el SINONIMO MÁS PLAUSIBLE que mantenga el MISMO sentido del modismo en el contexto dado.
4. El SINONIMO MÁS PLAUSIBLE debe:
   - Ser una palabra o frase simple y directa.
   - Tener máximo 10 palabras.
5. Define el sinónimo identificado.
6. No uses expresiones como: "significa", "se refiere a", "es cuando", "es aquella situación en la que".
7. Usa solo tu conocimiento interno (sin búsquedas externas).
8. Si desconoces el modismo, infiere el SINONIMO MÁS PLAUSIBLE según el contexto del ejemplo.

INPUT (JSON):
{
  "modismo": "{{modismo}}",
  "ejemplo": "{{ejemplo}}"
}

FORMATO DE SALIDA (JSON estricto):
{
  "input": {
    "modismo": "{{modismo}}",
    "ejemplo": "{{ejemplo}}"
  },
  "output": {
    "sinonimo": "<sinonimo más plausible>",
    "definicion": "<definición breve del sinonimo>"
  }
}
"""