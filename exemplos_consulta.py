import duckdb

con = duckdb.connect("mdcr_rs.duckdb")

# ============================================================
# 1. Visão geral do banco
# ============================================================
print("=" * 60)
print("TABELAS E REGISTROS")
print("=" * 60)
for row in con.execute("SHOW TABLES").fetchdf()['name']:
    n = con.execute("SELECT COUNT(*) FROM {}".format(row)).fetchone()[0]
    print("  {:<40} {:>12,} registros".format(row, n))

# ============================================================
# 2. Custeio total por ano — RS
# ============================================================
print("\n" + "=" * 60)
print("CUSTEIO TOTAL POR ANO (R$ bilhões)")
print("=" * 60)
print(con.execute("""
    SELECT AnoEmissao AS ano,
           COUNT(*) AS contratos,
           ROUND(SUM(VlCusteio)/1e9, 2) AS valor_bi
    FROM custeio_municipio_produto
    WHERE AnoEmissao != '2026'
    GROUP BY AnoEmissao
    ORDER BY AnoEmissao
""").fetchdf().to_string(index=False))

# ============================================================
# 3. Top 10 produtos por valor de custeio (série completa)
# ============================================================
print("\n" + "=" * 60)
print("TOP 10 PRODUTOS — CUSTEIO (série completa)")
print("=" * 60)
print(con.execute("""
    SELECT nomeProduto,
           COUNT(*) AS contratos,
           ROUND(SUM(VlCusteio)/1e9, 2) AS valor_bi,
           ROUND(100.0 * SUM(VlCusteio) / SUM(SUM(VlCusteio)) OVER (), 1) AS pct
    FROM custeio_municipio_produto
    GROUP BY nomeProduto
    ORDER BY valor_bi DESC
    LIMIT 10
""").fetchdf().to_string(index=False))

# ============================================================
# 4. Top 10 municípios por custeio em 2024
# ============================================================
print("\n" + "=" * 60)
print("TOP 10 MUNICÍPIOS — CUSTEIO 2024")
print("=" * 60)
print(con.execute("""
    SELECT Municipio,
           COUNT(*) AS contratos,
           ROUND(SUM(VlCusteio)/1e6, 1) AS valor_mi
    FROM custeio_municipio_produto
    WHERE AnoEmissao = '2024'
    GROUP BY Municipio
    ORDER BY valor_mi DESC
    LIMIT 10
""").fetchdf().to_string(index=False))

# ============================================================
# 5. Investimento por atividade e ano
# ============================================================
print("\n" + "=" * 60)
print("INVESTIMENTO POR ATIVIDADE E ANO")
print("=" * 60)
print(con.execute("""
    SELECT AnoEmissao AS ano,
           CASE Atividade WHEN '1' THEN 'Lavoura' ELSE 'Pecuaria' END AS atividade,
           COUNT(*) AS contratos,
           ROUND(SUM(VlInvest)/1e9, 2) AS valor_bi
    FROM investimento_municipio_produto
    WHERE AnoEmissao != '2026'
    GROUP BY AnoEmissao, Atividade
    ORDER BY AnoEmissao, Atividade
""").fetchdf().to_string(index=False))

# ============================================================
# 6. Crédito total por modalidade e ano (contratos_municipio)
# ============================================================
print("\n" + "=" * 60)
print("CRÉDITO TOTAL POR MODALIDADE E ANO (R$ bilhões)")
print("=" * 60)
print(con.execute("""
    SELECT AnoEmissao AS ano,
           ROUND(SUM(VlCusteio)/1e9, 2)          AS custeio_bi,
           ROUND(SUM(VlInvestimento)/1e9, 2)      AS invest_bi,
           ROUND(SUM(VlComercializacao)/1e9, 2)   AS comerc_bi,
           ROUND(SUM(VlIndustrializacao)/1e9, 2)  AS ind_bi,
           ROUND((SUM(VlCusteio)+SUM(VlInvestimento)+
                  SUM(VlComercializacao)+SUM(VlIndustrializacao))/1e9, 2) AS total_bi
    FROM contratos_municipio
    WHERE AnoEmissao != 2026
    GROUP BY AnoEmissao
    ORDER BY AnoEmissao
""").fetchdf().to_string(index=False))

# ============================================================
# 7. Soja — evolução por faixa de área (estrutura fundiária)
# ============================================================
print("\n" + "=" * 60)
print("SOJA — DISTRIBUIÇÃO POR FAIXA DE ÁREA (2024)")
print("=" * 60)
print(con.execute("""
    SELECT
        CASE
            WHEN AreaCusteio = 0       THEN '0 - sem area'
            WHEN AreaCusteio <= 50     THEN '1 - ate 50 ha'
            WHEN AreaCusteio <= 200    THEN '2 - 51 a 200 ha'
            WHEN AreaCusteio <= 500    THEN '3 - 201 a 500 ha'
            WHEN AreaCusteio <= 1000   THEN '4 - 501 a 1000 ha'
            ELSE                            '5 - acima 1000 ha'
        END AS faixa,
        COUNT(*) AS contratos,
        ROUND(SUM(VlCusteio)/1e6, 1) AS valor_mi,
        ROUND(AVG(AreaCusteio), 1) AS area_media_ha
    FROM custeio_municipio_produto
    WHERE nomeProduto ILIKE '%soja%'
      AND AnoEmissao = '2024'
    GROUP BY faixa
    ORDER BY faixa
""").fetchdf().to_string(index=False))

con.close()
print("\nConsultas concluidas.")
