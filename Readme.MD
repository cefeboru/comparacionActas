# Comparacion de Actas Presidenciales
Busca inconsistencias en las actas del TSE, 
## Notas
- Las actas contra las cuales se compara el resultado actual son del dia lunes (~Madugrada)
- Se compara la data contra el API del TSE https://api.tse.hn/prod/ApiActa/Consultar/1/[ID_ACTA]
- Actas al día lunes brindadas por [Kevin Lopez](https://www.facebook.com/kevinlkl3): ``` mongo ds127456-a0.mlab.com:27456/tse_dump -u geekshn -p Xv7YazDtp&L4Zbx ```

Generando un CSV que contiene las actas inconsistentes:
- Codigo de acta
- Departamento
- Municipio
- Votos Alianza (Actuales)
- Votos Nacional (Actuales)
- Votos Alianza (BACKUP)
- Votos Nacional (BACKUP)
