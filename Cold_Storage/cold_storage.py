{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "114eb263-9181-49c4-8706-89ac4c90ad3c",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "\n",
    "# Random seed for reproducibility\n",
    "np.random.seed(42)\n",
    "\n",
    "# We will create 1000 data points or rows\n",
    "num_rows = 1000"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "27b8a775",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Ambient Temperature\n",
    "ambient_temp = np.random.uniform(25, 45, num_rows)\n",
    "\n",
    "# Solar Irradiance\n",
    "solar_irradiance = np.random.uniform(0, 1000, num_rows)\n",
    "\n",
    "# Battery Health\n",
    "battery_health = np.random.uniform(60, 100, num_rows)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "3a21d412",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Adding some random noise to make the data more realistic\n",
    "noise = np.random.normal(0, 1, num_rows)\n",
    "\n",
    "# Target 1: Battery Discharge Rate (% per hour)\n",
    "\n",
    "battery_discharge_rate = (ambient_temp * 0.12) - (solar_irradiance * 0.008) + (100 - battery_health) * 0.05 + 10 + noise\n",
    "battery_discharge_rate = np.clip(battery_discharge_rate, 0, 100)\n",
    "\n",
    "# Target 2: Internal Cold Storage Temperature (°C)\n",
    "\n",
    "cold_storage_temp = 4.0 + (ambient_temp * 0.05) - (solar_irradiance * 0.002) + (noise * 0.2)\n",
    "cold_storage_temp = np.clip(cold_storage_temp, 1, 10) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "23bdb70c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "--- The first 5 rows of the dataset ---\n",
      "   Ambient_Temperature  Solar_Irradiance  Battery_Health  \\\n",
      "0            32.490802        185.132929       70.468227   \n",
      "1            44.014286        541.900947       69.879152   \n",
      "2            39.639879        872.945836       96.250183   \n",
      "3            36.973170        732.224886       69.981848   \n",
      "4            28.120373        806.561148       70.877989   \n",
      "\n",
      "   Battery_Discharge_Rate  Cold_Storage_Temp  \n",
      "0               14.954358           5.466262  \n",
      "1               13.069555           5.240314  \n",
      "2                8.644279           4.372816  \n",
      "3                8.713933           4.111018  \n",
      "4                9.590000           4.035285  \n",
      " The 'ecofreeze_data.csv' file has been created.\n"
     ]
    }
   ],
   "source": [
    "# Creating a dictionary\n",
    "data = {\n",
    "    'Ambient_Temperature': ambient_temp,\n",
    "    'Solar_Irradiance': solar_irradiance,\n",
    "    'Battery_Health': battery_health,\n",
    "    'Battery_Discharge_Rate': battery_discharge_rate,\n",
    "    'Cold_Storage_Temp': cold_storage_temp\n",
    "}\n",
    "\n",
    "# Creating a Pandas DataFrame\n",
    "df = pd.DataFrame(data)\n",
    "\n",
    "# Checking the first 5 rows of the dataset\n",
    "print(\"--- The first 5 rows of the dataset ---\")\n",
    "print(df.head())\n",
    "\n",
    "# Saving the DataFrame as a CSV file\n",
    "df.to_csv('ecofreeze_data.csv', index=False)\n",
    "print(\" The 'ecofreeze_data.csv' file has been created.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "80077b8e",
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.linear_model import LinearRegression\n",
    "import joblib\n",
    "\n",
    "# Loading the dataset\n",
    "df = pd.read_csv('ecofreeze_data.csv')\n",
    "\n",
    "# input feature and target variable\n",
    "X = df[['Ambient_Temperature', 'Solar_Irradiance', 'Battery_Health']]\n",
    "y_discharge = df['Battery_Discharge_Rate']\n",
    "y_temp = df['Cold_Storage_Temp']\n",
    "\n",
    "# Splitting the data into training and testing sets(80% train, 20% test)\n",
    "X_train, X_test, y_disharge_train, y_discharge_test = train_test_split(X, y_discharge, test_size=0.2, random_state=42)\n",
    "_, _, y_temp_train, y_temp_test = train_test_split(X, y_temp, test_size=0.2, random_state=42)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "dc32d9dd",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "🔋 Battery Model Accuracy: 82.74%\n",
      "❄️ Cold Storage Model Accuracy: 89.46%\n"
     ]
    }
   ],
   "source": [
    "# prediction models\n",
    "model_discharge = LinearRegression()\n",
    "model_discharge.fit(X_train, y_disharge_train)\n",
    "\n",
    "# predicting the cold storage temperature\n",
    "model_temp = LinearRegression()\n",
    "model_temp.fit(X_train, y_temp_train)\n",
    "\n",
    "# Model Accuracy (R² Score) \n",
    "print(f\"🔋 Battery Model Accuracy: {model_discharge.score(X_test, y_discharge_test) * 100:.2f}%\")\n",
    "print(f\"❄️ Cold Storage Model Accuracy: {model_temp.score(X_test, y_temp_test) * 100:.2f}%\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "6b1af3c2",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " 'model_discharge.pkl' and 'model_temp.pkl' have been saved successfully.\n"
     ]
    }
   ],
   "source": [
    "# Saving the models using joblib\n",
    "joblib.dump(model_discharge, 'model_discharge.pkl')\n",
    "joblib.dump(model_temp, 'model_temp.pkl')\n",
    "\n",
    "print(\" 'model_discharge.pkl' and 'model_temp.pkl' have been saved successfully.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "ec71da5e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'c:\\\\Users\\\\SheCoder\\\\Cold_storage'"
      ]
     },
     "execution_count": 1,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import os\n",
    "os.getcwd()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "base",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
