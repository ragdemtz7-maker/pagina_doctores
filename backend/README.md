# Backend de Citas Médicas

Este backend está construido en **Python Flask** y expone una API REST para gestionar pacientes, médicos y disponibilidad de citas.  
Se integra con **Amazon RDS (MySQL)** para persistencia de datos y puede desplegarse en AWS usando **Elastic Beanstalk** o **Lambda + API Gateway**.

---

## 🚀 Ejecutar en local

### 1. Crear entorno virtual
```sh
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 2. Instalar dependencias
```sh
pip install -r requirements.txt
```

### 3. Ejecutar en modo desarrollo
```sh
python -m backend.app
```
### 3.1 Ejecutar en modo desarrollo + swagger
```sh
python -m backend.app_swagger
```


### 4. Ejecutar en modo producción local con Gunicorn
```sh
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Despliegue en AWS

### Lambda + API Gateway (serverless)
Instalar Zappa:
```sh
pip install zappa
```

Inicializar:

```sh
zappa init
```

Desplegar:
```sh
zappa deploy dev
```

Esto crea un endpoint en API Gateway para tu backend Flask.
