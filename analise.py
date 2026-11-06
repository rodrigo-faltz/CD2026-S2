"""ECM514 — experimento CWRU. Execute: python analise.py"""
# %% Configuração
from pathlib import Path
import os, json, hashlib, platform, sys, importlib.metadata
os.environ.setdefault('MPLCONFIGDIR', '/tmp/cwru-matplotlib')
import numpy as np
import pandas as pd
import requests
from scipy.io import loadmat
from scipy.signal import resample_poly, welch
from scipy.stats import skew, kurtosis
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.svm import OneClassSVM, SVC
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (confusion_matrix, ConfusionMatrixDisplay, classification_report,
                             accuracy_score, f1_score, balanced_accuracy_score, roc_auc_score)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

ROOT = Path.cwd()
RAW = ROOT/'dados'/'raw'; OUT = ROOT/'resultados'
RAW.mkdir(parents=True, exist_ok=True); OUT.mkdir(exist_ok=True)
SEED = 42; FS = 12000; WINDOW = 2048
CLASSES = ['Normal','Pista interna','Esfera','Pista externa']
BASE_URL = 'https://engineering.case.edu/sites/default/files/'
EXPECTED_SHA256 = {'97': '16bf48babcf1c7ac224bc1a81cd9eafdb27e42d5cf559761907e067e8eeadf3c', '98': '37e6612c05e65c415dcfa2ab27a3fda648a5863160fa898b884a14743044e045', '99': '4b97e6b5361f45efb6951dc3b1aebcdb3b89cb69d0f96d6f5c297dd9f45eee75', '100': '88a5990cb541320e91505a1d72139e1993500ffe6e292a451011667f4138ca78', '105': 'f80b0ea04fd06b372a0eaec7c056543ea37e4bb4727a5b173d2a5bacd2aa9cab', '106': 'e5cec7cdd138e6cd1deb9ed8634e5aaa9bc1bd7094ddc075bff606580eb6e883', '107': '111ba8996a115684661a13c913bd74d8029a59294492f88aec7b03e175fdd388', '108': 'd415f0e65128bfa0b118c2051c988fb0dc6ce3e4c8aa45fdc5ad1d0967462e7d', '118': 'b00628f8dd8d1d930af77fa465d1e5cdb385fe259489053f91f3680bda7f640e', '119': 'bc72d9df7668219e004a0f711232b23ec0aed393eb9bd8f9f5483426f6b51330', '120': 'e0b7a584c49af52335ff0904a97d4afcf02d045625c582de63a7c85ce10b489c', '121': '52f686e984ba8e9b04a047a57416271cdb322cee57ee105dce58926a24b966cb', '130': '35a095307d0971477049b343a1b5981dde465a58fb7f233ad89b035068c1717d', '131': '7883f7b83beadc54b2f301767f9145ce07055707182fb0278fdf0a6bb53ce3cb', '132': '17a69ed5d2270b42532e678e35bbe2fa04a2cc413cf2bf9e88c7692de8662d18', '133': '53f076cb0d905cf46bffaee7736abce8224ffed777deed03c0c863d762a90c71', '169': 'f5448673725c4ea2735fe7d3fe4b16ad82b217eac6b62c4bf351c4549b0a5229', '170': 'bcb73a5208b67265468232a2e342f53719850901671d0ee28494f3af97621f46', '171': '63d0fdc1a68e64610ddfaf56a9c224d6137ab7b5c0d318eea1d542b9e5ffc029', '172': 'f75170ceef70d5da475671de0d2e52a0acd9b3883ad422b6deaf2907d888ba24', '185': '5bea2c60f177215ba3ec4ae287faf745d7e14aed1a12efe9e37b27c27044bafc', '186': '1b3b6f3ad38e891feaa8026fe957b34f62f9082785089cc74f6878acdfe88ec5', '187': '0f1338cce89beb5c8d8e5e154579bc576354e7c7d1617ebd1759662c6f3100b2', '188': '1981614324d653c2522bea68fd4fd87e337495b117d12596db67abd1e10e7443', '197': 'fa571b47cd942f9514a920b403fb7c053cd442bb2963a360a96d0f61432f03e9', '198': 'dbd58e4585ca8f8332c708b15936987ec0990ca701359fd2483dae2719df5b49', '199': 'ca4e6407fdb68845a6973da6028477911a62d018580063749fe956441be95cf2', '200': '2526483d2701220a700df8e6c9db0c527641b0887225907f4096610dd7120f4b', '209': '9f723d6d9d2eba714c6dc50f99321dffa73d8b1e4d3605675b2c2251511eff80', '210': '596692397e77e129a00f7b7a61c4c3ffd6c7a59979b89039e7f70a7431cce1c7', '211': '8296a02ee489c2d16cbd9fc278ca2e29b22475cec70ebe840558c78b6b743dc1', '212': 'bfe13761f545a26b217db897a12d27e16fec74306aa86ade8dbdc8ebe587c253', '222': 'fcc0ee740fa123b1f4683f555458891719efb2857afd9fdee63e8fde0ed14469', '223': '7287410fd2217e3b332c5ab4732a68963be046d7d17bd40efa41cabe6a0514e5', '224': '8a16894c2ff4d6bcdb9f4c345c0d5f13737b3bd6d15015d6b566c86e7a3ee7b7', '225': 'ece92fa141af03473fdfca80d00d9112472a20340224514e79979c6ddc97a6cf', '234': 'ebcbdb96612e8085bbdbf81f0e5e8e8a8d1a693d1ec559c4894f7792771aa9b2', '235': '667e4bf1f213f92d10dca71d494ad002d8fd22bfd8004b31a4c71ccf0d764b66', '236': 'c411d6d9826cba8073430555dc833e05fcbe4c38535f3eb7f03c525ea6797589', '237': '233d1edb2daa963658369119e389e30f02aca551dd7bb028ab33e7ba63edfd20'}
# Taxa do baseline não é codificada nos .mat; convenção 48 kHz, discutida no relatório.
NORMAL_FS = int(os.environ.get('CWRU_NORMAL_FS', '48000'))
assert NORMAL_FS in [12000, 48000]
rows = []
for load in range(4):
    rows.append(dict(file_id=97+load, classe='Normal', diametro_pol=0., carga_hp=load,
                     fs_original=NORMAL_FS, posicao='n/a'))
for diameter, starts in [(0.007,[105,118,130]),(0.014,[169,185,197]),(0.021,[209,222,234])]:
    for label, start in zip(CLASSES[1:], starts):
        for load in range(4):
            rows.append(dict(file_id=start+load, classe=label, diametro_pol=diameter,
                             carga_hp=load, fs_original=12000,
                             posicao='6 horas' if label=='Pista externa' else 'n/a'))
manifest = pd.DataFrame(rows)
manifest['split'] = manifest.carga_hp.map({0:'treino',1:'treino',2:'validacao',3:'teste'})
manifest['url'] = manifest.file_id.map(lambda i:f'{BASE_URL}{i}.mat')
assert len(manifest) == 40 and manifest.file_id.nunique() == 40

# %% Download e integridade
# Não cria dados sintéticos; falha explicitamente se o download ou canal estiver incorreto.
def download(row):
    dest = RAW/f'{row.file_id}.mat'
    if not dest.exists():
        for attempt in range(3):
            try:
                response = requests.get(row.url, timeout=90)
                response.raise_for_status()
                if not response.content.startswith(b'MATLAB'): raise ValueError('Resposta não é MAT')
                dest.write_bytes(response.content)
                break
            except (requests.RequestException, ValueError):
                if attempt == 2: raise
    actual_hash = hashlib.sha256(dest.read_bytes()).hexdigest()
    if actual_hash != EXPECTED_SHA256[str(row.file_id)]:
        raise ValueError(f'Integridade divergente: {dest}. Verifique a origem antes de continuar.')
    data = loadmat(dest)
    preferred = f'X{row.file_id:03d}_DE_time'
    channels = [preferred] if preferred in data else [key for key in data if key.endswith('_DE_time')]
    assert len(channels) == 1, (row.file_id, channels)
    x = data[channels[0]].ravel().astype(float)
    assert np.isfinite(x).all() and len(x) >= WINDOW
    rpm_preferred = f'X{row.file_id:03d}RPM'
    rpm_keys = [rpm_preferred] if rpm_preferred in data else [k for k in data if k.endswith('RPM')]
    return dict(file_id=row.file_id, sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
                bytes=dest.stat().st_size, canal=channels[0], n_original=len(x),
                rpm=float(data[rpm_keys[0]].ravel()[0]) if rpm_keys else None)
with ThreadPoolExecutor(max_workers=6) as pool:
    integrity = list(pool.map(download, manifest.itertuples(index=False)))
manifest = manifest.merge(pd.DataFrame(integrity), on='file_id')
manifest.to_csv(ROOT/'dados'/'manifesto.csv',index=False)
print('Arquivos reais verificados:',len(manifest))

# %% Janelamento e extração de atributos
# Split atribuído à gravação ANTES de janelar. Janelas contíguas sem sobreposição.
def features(x):
    z = x - np.mean(x)
    rms = np.sqrt(np.mean(z*z)); peak = np.max(np.abs(z)); mean_abs = np.mean(np.abs(z))
    f, p = welch(z, fs=FS, nperseg=512)
    p = p / max(p.sum(), 1e-20)
    centroid = np.sum(f*p)
    v = dict(rms=rms, pico_a_pico=np.ptp(z), pico=peak, assimetria=skew(z),
             curtose=kurtosis(z,fisher=False), fator_crista=peak/max(rms,1e-12),
             fator_forma=rms/max(mean_abs,1e-12), fator_impulso=peak/max(mean_abs,1e-12),
             centroide_hz=centroid, dispersao_hz=np.sqrt(np.sum((f-centroid)**2*p)),
             entropia_espectral=-np.sum(p*np.log(p+1e-20))/np.log(len(p)))
    for low in range(0,6000,1000):
        mask = (f>=low)&((f<low+1000) if low<5000 else (f<=6000))
        v[f'energia_rel_{low}_{low+1000}'] = p[mask].sum()
    return v
records = []
examples = {}
for row in manifest.itertuples(index=False):
    x = loadmat(RAW/f'{row.file_id}.mat')[row.canal].ravel()
    if row.fs_original != FS:
        assert row.fs_original == 4*FS
        x = resample_poly(x, up=1, down=4)  # filtro anti-aliasing polifásico
    if row.classe not in examples: examples[row.classe] = x[:WINDOW]
    n = len(x)//WINDOW
    for j in range(n):
        v = features(x[j*WINDOW:(j+1)*WINDOW])
        v.update(file_id=row.file_id, classe=row.classe, split=row.split,
                 carga_hp=row.carga_hp, diametro_pol=row.diametro_pol, janela=j)
        records.append(v)
frame = pd.DataFrame(records)
META = ['file_id','classe','split','carga_hp','diametro_pol','janela']
FEATURES = [c for c in frame if c not in META]
assert len(FEATURES)==17 and np.isfinite(frame[FEATURES].values).all()
sets = {s:frame[frame.split==s].copy() for s in ['treino','validacao','teste']}
for a,b in [('treino','validacao'),('treino','teste'),('validacao','teste')]:
    assert set(sets[a].file_id).isdisjoint(sets[b].file_id)
frame.to_csv(OUT/'atributos.csv',index=False)
counts = pd.crosstab(frame.classe,frame.split).reindex(CLASSES)
counts.to_csv(OUT/'contagens_janelas.csv')
print('Janelas por classe e partição:\n',counts)
tr, va, te = [sets[s] for s in ['treino','validacao','teste']]
Xtr, Xva, Xte = [s[FEATURES].values for s in [tr,va,te]]
ytr,yva,yte = [s.classe.values for s in [tr,va,te]]
binary_test = (yte!='Normal').astype(int)

# %% Modelos de detecção e diagnóstico
summary=[]; details={}; pred_frame=te[META].copy(); validation=[]
def evaluate(name, pred, diagnostic, score=None):
    pred_bin = (pred!='Normal').astype(int) if diagnostic else np.asarray(pred,dtype=int)
    tn,fp,fn,tp = confusion_matrix(binary_test,pred_bin,labels=[0,1]).ravel()
    info=dict(TN=int(tn),FP=int(fp),FN=int(fn),TP=int(tp),
              TPR=float(tp/(tp+fn)),FPR=float(fp/(fp+tn)))
    if score is not None: info['ROC_AUC']=float(roc_auc_score(binary_test,score))
    acc_class = 'não se aplica'
    if diagnostic:
        report=classification_report(yte,pred,labels=CLASSES,output_dict=True,zero_division=0)
        # "acurácia por classe" operacionalizada como recall da classe.
        acc_class='; '.join(f'{c}: {report[c]["recall"]:.4f}' for c in CLASSES)
        info.update(acuracia=float(accuracy_score(yte,pred)),
                    macro_f1=float(f1_score(yte,pred,average='macro')),
                    balanced_accuracy=float(balanced_accuracy_score(yte,pred)),relatorio=report)
        pd.DataFrame(report).T.to_csv(OUT/f'relatorio_{name}.csv')
        cm=confusion_matrix(yte,pred,labels=CLASSES)
        pd.DataFrame(cm,index=CLASSES,columns=CLASSES).to_csv(OUT/f'matriz_{name}.csv')
        fig,ax=plt.subplots(figsize=(8,6));ConfusionMatrixDisplay(cm,display_labels=CLASSES).plot(ax=ax,colorbar=False,cmap='Blues')
        ax.set(title=name,xlabel='Predição',ylabel='Classe real');plt.xticks(rotation=15)
    else:
        cm=np.array([[tn,fp],[fn,tp]])
        pd.DataFrame(cm,index=['Normal','Falha'],columns=['Normal','Falha']).to_csv(OUT/f'matriz_{name}.csv')
        fig,ax=plt.subplots(figsize=(6,5));ConfusionMatrixDisplay(cm,display_labels=['Normal','Falha']).plot(ax=ax,colorbar=False,cmap='Blues');ax.set_title(name)
    fig.tight_layout();fig.savefig(OUT/f'matriz_{name}.png',dpi=150);plt.close(fig)
    summary.append({'Dataset':'CWRU — recorte DE','Técnica':name,
                    'Tipo de falha identificada':'; '.join(CLASSES[1:]) if diagnostic else 'não se aplica',
                    'Taxa de detecção (TPR)':info['TPR'],'Falso positivo (FPR)':info['FPR'],
                    'Acurácia por classe (recall)':acc_class})
    details[name]=info;pred_frame[name]=pred

# Mesma padronização ajustada somente no normal de treino para os dois detectores.
normal_scaler=StandardScaler().fit(Xtr[ytr=='Normal'])
Ztrain=normal_scaler.transform(Xtr[ytr=='Normal'])
Zval=normal_scaler.transform(Xva[yva=='Normal']);Ztest=normal_scaler.transform(Xte)
for name, model in [('IsolationForest',IsolationForest(n_estimators=300,random_state=SEED,n_jobs=1)),
                    ('OneClassSVM',OneClassSVM(nu=0.05,gamma='scale'))]:
    model.fit(Ztrain)
    scores_val=-model.score_samples(Zval)
    threshold=float(np.quantile(scores_val,0.95,method='higher'))
    scores=-model.score_samples(Ztest)
    evaluate(name,scores>threshold,False,scores)
    details[name].update(limiar=threshold,FPR_validacao=float(np.mean(scores_val>threshold)))
# Busca pequena, pré-definida; seleção por macro-F1 na validação de carga 2 HP.
candidates={
 'RandomForest':[(f'folha={leaf}',RandomForestClassifier(n_estimators=300,min_samples_leaf=leaf,
             class_weight='balanced',random_state=SEED,n_jobs=1)) for leaf in [1,3,5]],
 'SVM_RBF':[(f'C={c}',make_pipeline(StandardScaler(),SVC(C=c,kernel='rbf',gamma='scale',class_weight='balanced'))) for c in [0.1,1,10]],
 'Baseline_dummy':[('most_frequent',DummyClassifier(strategy='most_frequent'))]}
for name, options in candidates.items():
    best_score=-1;best=None;param=None
    for label,model in options:
        model.fit(Xtr,ytr);valscore=f1_score(yva,model.predict(Xva),average='macro')
        validation.append(dict(modelo=name,parametros=label,macro_f1=valscore))
        if valscore>best_score:best_score=valscore;best=model;param=label
    # Sem refit em validação: protocolo conserva o limiar e distribuição de treino.
    evaluate(name,best.predict(Xte),True)
    details[name].update(parametros=param,macro_f1_validacao=float(best_score))
    if name=='RandomForest':
        pd.Series(best.feature_importances_,index=FEATURES).sort_values(ascending=False).to_csv(OUT/'importancia_rf.csv',header=['importancia_impureza'])
summary=pd.DataFrame(summary);summary.to_csv(OUT/'tabela_resumo.csv',index=False)
pd.DataFrame(validation).to_csv(OUT/'selecao_validacao.csv',index=False)
pred_frame.to_csv(OUT/'predicoes_teste.csv',index=False)
(OUT/'metricas.json').write_text(json.dumps(details,ensure_ascii=False,indent=2))
# Desempenho por gravação: revela heterogeneidade sem assumir janelas independentes.
file_results=[]
for fid,g in pred_frame.groupby('file_id'):
    for name in details:
        good=(g[name].values==g.classe.values) if name in candidates else (g[name].values==(g.classe.values!='Normal'))
        file_results.append(dict(file_id=int(fid),classe=g.classe.iloc[0],modelo=name,n_janelas=len(g),fracao_correta=float(np.mean(good))))
pd.DataFrame(file_results).to_csv(OUT/'desempenho_por_gravacao.csv',index=False)

# %% Visualização e proveniência
fig,axes=plt.subplots(4,2,figsize=(12,11))
for i,(label,x) in enumerate(examples.items()):
    axes[i,0].plot(np.arange(len(x))/FS,x,linewidth=.6);axes[i,0].set(title=label,xlabel='Tempo (s)',ylabel='Aceleração (unidade da fonte)')
    f,p=welch(x-np.mean(x),fs=FS,nperseg=512)
    axes[i,1].semilogy(f,p+1e-20);axes[i,1].set(xlabel='Frequência (Hz)',ylabel='PSD')
fig.tight_layout();fig.savefig(OUT/'sinais_espectros.png',dpi=150);plt.close(fig)
versions={p:importlib.metadata.version(p) for p in ['numpy','scipy','pandas','scikit-learn','matplotlib','requests']}
(OUT/'ambiente.json').write_text(json.dumps(dict(python=sys.version,plataforma=platform.platform(),pacotes=versions,
        seed=SEED,janela=WINDOW,fs=FS,normal_fs=NORMAL_FS,features=FEATURES),ensure_ascii=False,indent=2))
(OUT/'tabela_resumo.md').write_text(summary.to_markdown(index=False,floatfmt='.4f'))
print(summary.to_string(index=False));print('Resultados salvos em',OUT)
