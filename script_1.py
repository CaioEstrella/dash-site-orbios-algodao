# Criar um arquivo GeoJSON simplificado dos estados brasileiros
# Este é um exemplo com coordenadas aproximadas - em um projeto real, usaria dados do IBGE

import json

# GeoJSON simplificado dos estados brasileiros
# Em um projeto real, você baixaria o arquivo completo do IBGE ou outras fontes
geojson_brasil = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "MT",
            "properties": {
                "name": "Mato Grosso",
                "sigla": "MT",
                "regiao": "Centro-Oeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-65.0, -7.0], [-50.0, -7.0], [-50.0, -18.0], [-65.0, -18.0], [-65.0, -7.0]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "BA",
            "properties": {
                "name": "Bahia",
                "sigla": "BA",
                "regiao": "Nordeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-46.5, -8.5], [-37.0, -8.5], [-37.0, -18.5], [-46.5, -18.5], [-46.5, -8.5]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "GO",
            "properties": {
                "name": "Goiás",
                "sigla": "GO",
                "regiao": "Centro-Oeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-53.0, -12.0], [-45.5, -12.0], [-45.5, -19.5], [-53.0, -19.5], [-53.0, -12.0]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "MS",
            "properties": {
                "name": "Mato Grosso do Sul",
                "sigla": "MS",
                "regiao": "Centro-Oeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-58.0, -17.0], [-50.0, -17.0], [-50.0, -24.0], [-58.0, -24.0], [-58.0, -17.0]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "MA",
            "properties": {
                "name": "Maranhão",
                "sigla": "MA",
                "regiao": "Nordeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-48.0, -1.0], [-41.0, -1.0], [-41.0, -10.0], [-48.0, -10.0], [-48.0, -1.0]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "PI",
            "properties": {
                "name": "Piauí",
                "sigla": "PI",
                "regiao": "Nordeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-46.0, -2.5], [-40.0, -2.5], [-40.0, -11.0], [-46.0, -11.0], [-46.0, -2.5]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "CE",
            "properties": {
                "name": "Ceará",
                "sigla": "CE",
                "regiao": "Nordeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-41.5, -2.5], [-37.0, -2.5], [-37.0, -8.0], [-41.5, -8.0], [-41.5, -2.5]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "MG",
            "properties": {
                "name": "Minas Gerais",
                "sigla": "MG",
                "regiao": "Sudeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-51.0, -14.0], [-39.0, -14.0], [-39.0, -22.5], [-51.0, -22.5], [-51.0, -14.0]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "SP",
            "properties": {
                "name": "São Paulo",
                "sigla": "SP",
                "regiao": "Sudeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-53.0, -19.5], [-44.0, -19.5], [-44.0, -25.5], [-53.0, -25.5], [-53.0, -19.5]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "PR",
            "properties": {
                "name": "Paraná",
                "sigla": "PR",
                "regiao": "Sul"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-55.0, -22.0], [-48.0, -22.0], [-48.0, -27.0], [-55.0, -27.0], [-55.0, -22.0]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "TO",
            "properties": {
                "name": "Tocantins",
                "sigla": "TO",
                "regiao": "Norte"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-50.5, -5.0], [-45.0, -5.0], [-45.0, -13.0], [-50.5, -13.0], [-50.5, -5.0]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "PA",
            "properties": {
                "name": "Pará",
                "sigla": "PA",
                "regiao": "Norte"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-59.0, 2.0], [-46.0, 2.0], [-46.0, -13.0], [-59.0, -13.0], [-59.0, 2.0]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "AL",
            "properties": {
                "name": "Alagoas",
                "sigla": "AL",
                "regiao": "Nordeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-38.5, -8.5], [-35.0, -8.5], [-35.0, -10.5], [-38.5, -10.5], [-38.5, -8.5]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "PB",
            "properties": {
                "name": "Paraíba",
                "sigla": "PB",
                "regiao": "Nordeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-39.0, -6.0], [-34.5, -6.0], [-34.5, -8.5], [-39.0, -8.5], [-39.0, -6.0]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "RN",
            "properties": {
                "name": "Rio Grande do Norte",
                "sigla": "RN",
                "regiao": "Nordeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-38.5, -4.5], [-34.5, -4.5], [-34.5, -7.0], [-38.5, -7.0], [-38.5, -4.5]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "PE",
            "properties": {
                "name": "Pernambuco",
                "sigla": "PE",
                "regiao": "Nordeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-41.5, -7.0], [-34.5, -7.0], [-34.5, -9.5], [-41.5, -9.5], [-41.5, -7.0]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "SE",
            "properties": {
                "name": "Sergipe",
                "sigla": "SE",
                "regiao": "Nordeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-38.5, -10.0], [-36.5, -10.0], [-36.5, -11.5], [-38.5, -11.5], [-38.5, -10.0]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "RO",
            "properties": {
                "name": "Rondônia",
                "sigla": "RO",
                "regiao": "Norte"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-66.0, -7.5], [-60.0, -7.5], [-60.0, -13.5], [-66.0, -13.5], [-66.0, -7.5]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "DF",
            "properties": {
                "name": "Distrito Federal",
                "sigla": "DF",
                "regiao": "Centro-Oeste"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-48.5, -15.3], [-47.0, -15.3], [-47.0, -16.2], [-48.5, -16.2], [-48.5, -15.3]
                ]]
            }
        }
    ]
}

# Salvar arquivo GeoJSON
with open('brasil_estados_poligonos.geojson', 'w') as f:
    json.dump(geojson_brasil, f)

print("Arquivo GeoJSON criado: brasil_estados_poligonos.geojson")
print(f"Total de estados no GeoJSON: {len(geojson_brasil['features'])}")