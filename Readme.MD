# Comparacion de Actas Presidenciales
Busca inconsistencias en las actas, el output tendra este formato:
- Codigo de acta
- Votos Alianza (Actuales)
- Votos Nacional (Actuales)
- Votos Alianza (Lunes)
- Votos Nacional (Lunes)
## Notas
- Las actas contra las cuales se compara el resultado actual son del dia lunes (~Madugrada)
- Se compara contra la data en [VotoSocial2017](http://votosocial2017.herokuapp.com/#_=_) (CSV)
- Actas lunes brindadas por [Kevin Lopez](https://www.facebook.com/kevinlkl3): ``` mongo ds127456-a0.mlab.com:27456/tse_dump -u geekshn -p Xv7YazDtp&L4Zbx ```