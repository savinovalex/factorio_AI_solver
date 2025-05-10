cd build

cmake  -DPYBIND11_PYTHON_VERSION=3.10 ..

make

cd ..

sh run_tests.sh