# -*- coding: utf-8 -*-
"""
PDF 多页拆分脚本
按指定页数（默认 200 页）为单位拆分 PDF 文件。
用法：修改下方 PDF 路径后直接运行：python split_pdf.py
依赖：pip install pypdf
"""

import os

from pypdf import PdfReader, PdfWriter

# ==================== 可修改配置 ====================
# 待拆分的 PDF 文件路径（改成你自己的文件）
一pdf_path = r"D:\program\tencent\wechatfile\xwechat_files\wxid_unqy9iv7qjnr21_2542\msg\file\2026-09\电力市场政策汇编（截至2026.3）.pdf"

# 拆分后输出目录
output_dir = r"D:\project\IIA\tmp"

# 每个分片包含的页数
pages_per_chunk = 200
# ===================================================


def split_pdf(pdf_path: str, out_dir: str, chunk_size: int) -> list[str]:
    """将 pdf_path 按 chunk_size 页为单位拆分，返回生成的文件路径列表。"""
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    if total_pages == 0:
        raise ValueError(f"PDF 为空或无法读取：{pdf_path}")

    os.makedirs(out_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    generated = []
    for start in range(0, total_pages, chunk_size):
        end = min(start + chunk_size, total_pages)
        writer = PdfWriter()
        for page in reader.pages[start:end]:
            writer.add_page(page)

        chunk_num = start // chunk_size + 1
        out_path = os.path.join(out_dir, f"{base_name}_第{chunk_num:03d}部分_第{start + 1}-{end}页.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
        generated.append(out_path)
        print(f"[{chunk_num}] 已生成：{out_path}（共 {end - start} 页）")

    return generated


if __name__ == "__main__":
    files = split_pdf(一pdf_path, output_dir, pages_per_chunk)
    print(f"\n完成！共拆分出 {len(files)} 个文件，输出目录：{output_dir}")
