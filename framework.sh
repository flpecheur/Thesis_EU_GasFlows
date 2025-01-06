#!/bin/bash

echo "=== Gas Flow Framework ==="
echo "1. Collect data"
echo "2. Prepare data "
echo "3. View inter-country data map"
echo "4. View country totals map"
echo "5. View LNG point data map for 2019"
echo "6. View LNG point data map for 2023"
echo "7. Exit"
read -p "Enter your choice: " choice

case $choice in
  1) python src/entsogData.py ;;
  2) python src/buildDataPerCountry.py && python src/buildDataPerPointType.py ;;
  3) python src/mapPairs.py ;;
  4) python src/mapCountryTotals_FINAL.py ;;
  5) python src/mapLNG_2019.py ;;
  5) python src/mapLNG_2023.py ;;
  0) echo "Exiting..." ;;
  *) echo "Invalid choice" ;;
esac
