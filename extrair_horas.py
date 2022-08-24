import datetime
import time

import pandas as pd
from tqdm import tqdm

from help_functions import (clean_screen, find_elements_by_class_name,
                            iniciate_chromedriver)

TODAY = str(datetime.datetime.now().date())

def tratar_horas(tempo_jogado: str) -> float:
    if tempo_jogado == '0':
        return float(0)
    
    if 'h' in tempo_jogado and 'm' in tempo_jogado:
        horas = tempo_jogado.split('h')[0]
        minutos = str(tempo_jogado.split('h')[-1]).replace('m', '')
        return float(horas) + float(minutos) / 60

    if 'h' in tempo_jogado:
        horas = tempo_jogado.split('h')[0]
        return horas
    
    if 's' in tempo_jogado:
        minutos = tempo_jogado.split('m')[0]
        segundos = str(tempo_jogado.split('m')[1]).replace('s', '')
        return float(minutos)/60 + float(segundos) / 3600

    return tempo_jogado


def coletar_dados(driver, URL: str, modo_jogo: str) -> pd.DataFrame:
    driver.get(URL)

    df = pd.DataFrame()
    nomes_agentes_element = find_elements_by_class_name(driver=driver, class_name='agent__name-name')
    horas_agentes_element = find_elements_by_class_name(driver=driver, class_name='agent__name-time')

    lista_nomes_agentes = []
    for nome_agente in nomes_agentes_element:
        lista_nomes_agentes.append(nome_agente.text)

    lista_horas_agentes = []
    for horas_agentes in horas_agentes_element:
        lista_horas_agentes.append(horas_agentes.text)

    # Montando dataframe
    df['AGENTE'] = lista_nomes_agentes
    df[modo_jogo] = lista_horas_agentes


    # Tratamento dos dados
    df[modo_jogo] = df[modo_jogo].apply(lambda x: x.replace('Played ', ''))
    df[modo_jogo] = df[modo_jogo].apply(lambda x: tratar_horas(x))


    return df


def main():
    df_final = pd.DataFrame()

    nick = ''

    URL_COMPETITIVE = f'https://tracker.gg/valorant/profile/riot/{nick}/agents?season=all'
    URL_DEATHMATCH = f'https://tracker.gg/valorant/profile/riot/{nick}/agents?playlist=deathmatch&season=all'
    URL_ESCALATION = f'https://tracker.gg/valorant/profile/riot/{nick}/agents?playlist=escalation&season=all'
    URL_REPLICATION = f'https://tracker.gg/valorant/profile/riot/{nick}/agents?playlist=replication&season=all'
    URL_SNOWBALL_FIGHT = f'https://tracker.gg/valorant/profile/riot/{nick}/agents?playlist=snowball&season=all'
    URL_SPIKE_RUSH = f'https://tracker.gg/valorant/profile/riot/{nick}/agents?playlist=spikerush&season=all'
    URL_UNRATED = f'https://tracker.gg/valorant/profile/riot/{nick}/agents?playlist=unrated&season=all'

    driver = iniciate_chromedriver()
    
    time.sleep(5)

    # Coleta dos dados
    df_competitivo = coletar_dados(driver, URL_COMPETITIVE, 'Competitivo')
    df_deathmatch = coletar_dados(driver, URL_DEATHMATCH, 'Deathmatch')
    df_escalation = coletar_dados(driver, URL_ESCALATION, 'Escalation')
    df_replication = coletar_dados(driver, URL_REPLICATION, 'Replication')
    df_snowball = coletar_dados(driver, URL_SNOWBALL_FIGHT, 'Snowball Fight')
    df_spike_rush = coletar_dados(driver, URL_SPIKE_RUSH, 'Spike Rush')
    df_unrated = coletar_dados(driver, URL_UNRATED, 'Unrated')

    # Concatenando os dataframes
    df_final = pd.merge(df_competitivo, df_deathmatch, on='AGENTE', how='outer')
    df_final = pd.merge(df_final, df_escalation, on='AGENTE', how='outer')
    df_final = pd.merge(df_final, df_replication, on='AGENTE', how='outer')
    df_final = pd.merge(df_final, df_snowball, on='AGENTE', how='outer')
    df_final = pd.merge(df_final, df_spike_rush, on='AGENTE', how='outer')
    df_final = pd.merge(df_final, df_unrated, on='AGENTE', how='outer')
    df_final = df_final.fillna(0)

    print(df_final)

    df_final.to_csv('outputs/Base_Tracker_GG.csv', index=False)

    driver.quit()

if __name__ == '__main__':
    clean_screen()
    main()
