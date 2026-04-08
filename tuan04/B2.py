def xuat_cac_dinh(graph):
    # Sử dụng set để lưu các đỉnh (đảm bảo không bị trùng lặp)
    danh_sach_dinh = set()

    for dinh_nguon, dinh_ke in graph.items():
        danh_sach_dinh.add(dinh_nguon)  # Thêm đỉnh nguồn
        for dinh_den in dinh_ke:
            danh_sach_dinh.add(dinh_den)  # Thêm các đỉnh đích kề với nó

    # Sắp xếp theo thứ tự bảng chữ cái
    dinh_sap_xep = sorted(list(danh_sach_dinh))

    # In ra định dạng chuỗi
    print(" ".join(dinh_sap_xep))

