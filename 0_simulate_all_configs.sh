for f in $(ls "$(pwd)/Prefabs/configs/"); do
 NEWFILENAME=$(echo $f | sed -e 's/\-config.json//g');
 NEWFILENAMEEXT="$NEWFILENAME-output.json";
 echo "Executing -> $f - Will save as -> $NEWFILENAMEEXT";
 python -u CLI.py --prefab "$NEWFILENAME" --save-simulation "$(pwd)/Prefabs/outputs/$NEWFILENAMEEXT" --skip-summary --skip-save-config --simulate
done
