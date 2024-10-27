from io_handler import check_read_write_dirs, clean_public_directory, push_public

def main():
    check_read_write_dirs()
    clean_public_directory()
    push_public()


main()