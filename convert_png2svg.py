import asyncio
from pathlib import Path
from svgtrace import trace, asyncTrace, skimageTrace
from PIL import Image
import time

# input_file_path = "/home/pop/development/demos/ocr_service/samples/"
# input_file = input_file_path + "receipt_with_barcode.png"
# output_file = "samples/receipt_with_barcode_py"
# t0 = time.perf_counter()

# svg_output1 = trace(input_file, True)
# Path(output_file + "-bw.svg").write_text(svg_output1, encoding="utf-8")
# t1 = time.perf_counter() - t0
# print("test-1 took ", t1)


# input_file = input_file_path + "rpower-pos-asian-restaurant-receipt.png"
# output_file = "samples/rpower-pos-asian-restaurant-receipt_py"
# t0 = time.perf_counter()
# Path(output_file + "-asyncBw.svg").write_text(
#     asyncio.run(asyncTrace(input_file, True)), encoding="utf-8"
# )
# t1 = time.perf_counter() - t0
# print("test-2 took ", t1)


input_file="/home/pop/development/demos/ocr_service/result/invoice1.png"
output_file="result/invoice1.svg"
t0 = time.perf_counter()
Path(output_file).write_text(
    asyncio.run(asyncTrace(input_file, True)), encoding="utf-8"
)
t1 = time.perf_counter() - t0
print("test-2 took ", t1)


# t0 = time.perf_counter()
# Path(output_file+"-skimageBw.svg").write_text(skimageTrace(Image.open(input_file)), encoding="utf-8")
# t1 = time.perf_counter() - t0
# print("test-3 took ", t1)
