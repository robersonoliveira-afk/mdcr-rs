# Banco de Dados de Crédito Rural — Rio Grande do Sul

Banco de dados de crédito rural do Rio Grande do Sul construído a partir da API pública do Banco Central do Brasil (MDCR/SICOR), cobrindo o período de 2013 a maio/2026.

## Sobre o projeto

Este banco foi desenvolvido como base empírica para pesquisa sobre alocação de crédito rural, risco agrícola e dinâmica territorial no Pampa gaúcho, no âmbito de tese de professor titular (UFSM). Os dados permitem análises territoriais desagregadas por município, produto, programa e modalidade de crédito.

## Estrutura do banco

Arquivo único: `mdcr_rs.duckdb`
Total de registros: ~2,1 milhões
Período: janeiro/2013 a maio/2026
Unidade territorial: municípios do Rio Grande do Sul (497)

### Tabela 1 — `custeio_municipio_produto`

787.055 registros. Nível de detalhe: município × produto × mês.

| Variável | Descrição |
|----------|-----------|
| `Municipio` | Nome do município |
| `codIbge` | Código IBGE do município |
| `codCadMu` | Código cadastral BCB |
| `nomeProduto` | Produto financiado (soja, bovinos, arroz...) |
| `cdProduto` | Código do produto |
| `Atividade` | 1 = lavoura / 2 = pecuária |
| `MesEmissao` | Mês de emissão |
| `AnoEmissao` | Ano de emissão |
| `cdPrograma` | Código do programa (Pronaf, Pronamp...) |
| `cdSubPrograma` | Código do subprograma |
| `cdFonteRecurso` | Fonte (controlado, livre, BNDES) |
| `cdModalidade` | Modalidade do contrato |
| `cdTipoSeguro` | Tipo de seguro vinculado |
| `VlCusteio` | Valor contratado (R$) |
| `AreaCusteio` | Área financiada (ha) |

### Tabela 2 — `investimento_municipio_produto`

542.211 registros. Nível de detalhe: município × produto × mês.

| Variável | Descrição |
|----------|-----------|
| `Municipio` | Nome do município |
| `cdMunicipio` | Código cadastral BCB |
| `nomeProduto` | Produto/finalidade do investimento |
| `cdProduto` | Código do produto |
| `Atividade` | 1 = lavoura / 2 = pecuária |
| `MesEmissao` | Mês de emissão |
| `AnoEmissao` | Ano de emissão |
| `cdPrograma` | Código do programa |
| `cdSubPrograma` | Código do subprograma |
| `cdFonteRecurso` | Fonte de recurso |
| `cdModalidade` | Modalidade |
| `cdTipoSeguro` | Tipo de seguro |
| `VlInvest` | Valor investido (R$) |
| `AreaInvest` | Área financiada (ha) |

### Tabela 3 — `contratos_municipio`

782.015 registros. Nível de detalhe: município × mês — visão consolidada de todas as modalidades.

| Variável | Descrição |
|----------|-----------|
| `Municipio` | Nome do município |
| `cdMunicipio` | Código cadastral BCB |
| `codMunicIbge` | Código IBGE do município |
| `nomeUF` | Unidade federativa (RS) |
| `MesEmissao` | Mês de emissão |
| `AnoEmissao` | Ano de emissão |
| `cdPrograma` | Código do programa |
| `cdSubPrograma` | Código do subprograma |
| `cdFonteRecurso` | Fonte de recurso |
| `Atividade` | 1 = lavoura / 2 = pecuária |
| `QtdCusteio` / `VlCusteio` | Quantidade e valor de custeio |
| `QtdInvestimento` / `VlInvestimento` | Quantidade e valor de investimento |
| `QtdComercializacao` / `VlComercializacao` | Quantidade e valor de comercialização |
| `QtdIndustrializacao` / `VlIndustrializacao` | Quantidade e valor de industrialização |
| `AreaCusteio` / `AreaInvestimento` | Áreas financiadas (ha) |

## Dados do Brasil inteiro

Além do banco filtrado para o RS, o arquivo `Contratos por Município.json` (2,2 GB) contém os dados nacionais completos com ~5 milhões de registros. Disponível para análises comparativas entre estados.

## Pré-requisitos

```bash
pip install duckdb pandas
```

Python 3.10 ou superior.

## Como usar

```python
import duckdb

con = duckdb.connect("mdcr_rs.duckdb")

# listar tabelas
print(con.execute("SHOW TABLES").fetchdf())

# exemplo: custeio de soja por município em 2024
df = con.execute("""
    SELECT Municipio, ROUND(SUM(VlCusteio)/1e6, 2) AS valor_mi
    FROM custeio_municipio_produto
    WHERE nomeProduto ILIKE '%soja%'
      AND AnoEmissao = '2024'
    GROUP BY Municipio
    ORDER BY valor_mi DESC
    LIMIT 10
""").fetchdf()

print(df)
con.close()
```

Ver arquivo `exemplos_consulta.py` para mais exemplos.

## Fonte

Banco Central do Brasil — Matriz de Dados do Crédito Rural (MDCR/SICOR)
API: https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata/
Dados abertos sob licença Open Data Commons Open Database License (ODbL)

## Autoria

Prof. Róberson Macedo de Oliveira
Colégio Politécnico da UFSM — Eixo Recursos Naturais
roberson.oliveira@ufsm.br

Uso livre para fins acadêmicos e educacionais com citação da fonte.
