cmake CMakeLists.txt
make
python3 setup.py build

P=$(ls -d build/lib*)
for fn in `ls $P`; do mv $P/$fn ai/$(echo $fn | cut -d'.' -f 1).so; done
