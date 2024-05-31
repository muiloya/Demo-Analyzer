import utils
import scoreboardgenerator

def main():
    while True:
        file_path = input("Enter the path to your demo file: ")
        ##TODO: add function to filter filepath for windows, linux, MAC. Especially for drag drop file to terminal.
        print(file_path)
        if not utils.check_file_exists(file_path):
            print("Unable to find file, please check your path and try again")
            continue
        if not utils.is_valid_file_type(file_path):
            print("Invalid file type, ensure .dem or .dem.gz file")
            continue
        file_type = utils.get_file_type(file_path)
        if(file_type) == "gz":
            file_path = utils.extract_dem_from_gz(file_path)
        parser = utils.open_demo(file_path)
        scoreboardgenerator.ScoreboardGenerator(parser)
        if(file_type) == "gz":
            utils.delete_file(file_path)

if __name__ == "__main__":
    main()