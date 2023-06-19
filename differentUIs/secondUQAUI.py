import sys
import inquirer

import queries


def display_batches():
    batch_id = input("Enter the batch ID: ")
    batches = queries.get_batches(batch_id)
    if batches:
        print("Batch ID | Batch Name | Load Status | Record Stage | Admin Count | Score Count")
        for batch in batches:
            print(f"{batch[0]} | {batch[1]} | {batch[2]} | {batch[3]} | {batch[4]} | {batch[5]}")
    else:
        print("No batches found.")


def display_rejects():
    process_id = input("Enter the process ID: ")
    rejects = queries.get_rejects(process_id)
    if rejects:
        print("Process ID | Process Name | Reject Message | Reject Count")
        for reject in rejects:
            print(f"{reject[0]} | {reject[1]} | {reject[2]} | {reject[3]}")
    else:
        print("No rejects found.")


def display_medium_matches():
    batch_id = input("Enter the batch ID: ")
    matches = queries.get_medium_matches(batch_id)
    if matches:
        print("First Name | Middle Name | Last Name | Grade | Birthdate | Source School Code | Source Student ID | Mapped Student ID | Mapped State Student ID | Batch Name | Student Identity UUID")
        for match in matches:
            print(f"{match[0]} | {match[1]} | {match[2]} | {match[3]} | {match[4]} | {match[5]} | {match[6]} | {match[7]} | {match[8]} | {match[9]} | {match[10]}")
    else:
        print("No medium matches found.")


def display_unmapped_schools():
    batch_id = input("Enter the batch ID: ")
    schools = queries.get_unmapped_schools(batch_id)
    if schools:
        print("School Identity UUID | State Code | Local School Code | School Name")
        for school in schools:
            print(f"{school[0]} | {school[1]} | {school[2]} | {school[3]}")
    else:
        print("No unmapped schools found.")


def main():
    while True:
        print("Unified QA 1.0")
        questions = [
            inquirer.List(
                "option",
                message="Select an option:",
                choices=[
                    ("Get batches", display_batches),
                    ("Get rejects", display_rejects),
                    ("Get medium matches", display_medium_matches),
                    ("Get unmapped schools", display_unmapped_schools),
                    ("Exit", sys.exit),
                ],
            )
        ]
        answers = inquirer.prompt(questions)
        selected_option = answers["option"]
        selected_option()


if __name__ == "__main__":
    main()
