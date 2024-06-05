import utils
import scoreboardgenerator

def main():
    while True:
        file_path = input("Enter the path to your demo file: ")
        file_path = utils.clean_file_path(file_path)
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
        scoreboard = scoreboardgenerator.ScoreboardGenerator(parser)
        user_response = input("Export scoreboard to CSV? (Y/N): ")
        if user_response.lower() == "y":
            if utils.export_to_csv(scoreboard):
                print("Exported to output.csv")
            else: print("Access Denied: Close output.csv and try again")
        if(file_type) == "gz":
            utils.delete_file(file_path)

if __name__ == "__main__":
    main()