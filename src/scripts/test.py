import os
import sys
import atexit
import argparse
from typing import Union

from jinja2 import Template

tests_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(tests_path)

from tests import Assignment
from tests import test_assignment_1_1, test_assignment_1_2, test_assignment_1_3
from tests import test_assignment_2_1
from tests import (
    test_assignment_3_1,
    test_assignment_3_2,
    test_assignment_3_3,
    test_assignment_3_4,
)
from tests import (
    test_assignment_4_1,
    test_assignment_4_2,
    test_assignment_4_3,
    test_assignment_4_4,
)

PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir)
)
MAX_POINTS = 10
MODULES = [
    "tuning",
    "knn_classifier",
    "mlp_classifier",
    "linear_classifier"
]

RESULT = {
    "success": True,
    "total_points": 0,
    "failure_message": "",
    "max_points": MAX_POINTS,
}

def create_assignments(dataset_dir: str) -> list:
    return [
        Assignment(
            name="assignment_1_1",
            test_func=test_assignment_1_1,
            verification_file=os.path.join(dataset_dir, "assignment_1_1.npy"),
        ),
        Assignment(
            name="assignment_1_2",
            test_func=test_assignment_1_2,
            verification_file=os.path.join(dataset_dir, "assignment_1_2.npy"),
        ),
        Assignment(
            name="assignment_1_3",
            test_func=test_assignment_1_3,
            verification_file=os.path.join(dataset_dir, "assignment_1_3.npy"),
        ),
        Assignment(
            name="assignment_2_1",
            test_func=test_assignment_2_1,
            verification_file=os.path.join(dataset_dir, "assignment_2_1.npy"),
        ),
        Assignment(
            name="assignment_3_1",
            test_func=test_assignment_3_1,
            verification_file=os.path.join(dataset_dir, "assignment_3_1.pt"),
        ),
        Assignment(
            name="assignment_3_2",
            test_func=test_assignment_3_2,
            verification_file=os.path.join(dataset_dir, "assignment_3_2.pt"),
        ),
        Assignment(
            name="assignment_3_3",
            test_func=test_assignment_3_3,
            verification_file=os.path.join(dataset_dir, "assignment_3_3.pt"),
        ),
        Assignment(
            name="assignment_3_4",
            test_func=test_assignment_3_4,
            verification_file=os.path.join(dataset_dir, "assignment_3_4.pt"),
        ),
        Assignment(
            name="assignment_4_1",
            test_func=test_assignment_4_1,
            verification_file=os.path.join(dataset_dir, "assignment_4_1.pt"),
        ),
        Assignment(
            name="assignment_4_2",
            test_func=test_assignment_4_2,
            verification_file=os.path.join(dataset_dir, "assignment_4_2.pt"),
        ),
        Assignment(
            name="assignment_4_3",
            test_func=test_assignment_4_3,
            verification_file=os.path.join(dataset_dir, "assignment_4_3.pt"),
        ),
        Assignment(
            name="assignment_4_4",
            test_func=test_assignment_4_4,
            verification_file=os.path.join(dataset_dir, "assignment_4_4.pt"),
        ),
    ]

def exit_handler(student_dir: str) -> None:
    """This function is called when the program exits.
    It makes sure that the results are saved no
    matter what happens.
    """
    sys.stdout.flush()

    if RESULT["success"]:
        template_file = os.path.join(PROJECT_DIR, "data", "templates", "success_template.html")
    else:
        template_file = os.path.join(PROJECT_DIR, "data", "templates", "failure_template.html")

    with open(template_file, 'r') as f:
        template = Template(f.read())

    rendered_html = template.render(**RESULT)


    if os.path.isdir(student_dir):
        txt_results = os.path.join(student_dir, "results.txt")
        html_results = os.path.join(student_dir, "results.html")

        with open(txt_results, "w") as f:
            f.write(str(RESULT["total_points"]))

        with open(html_results, "w") as f:
            f.write(rendered_html)


def text_color(points: Union[int, float], max_points: Union[int, float]) -> str:
    """This function returns the color of the text (in Bootstrap format) based on the number of points.

    Args:
        points (Union[int, float]): The number of points.
        max_points (Union[int, float]): The maximum number of points.

    Returns:
        str: The color of the text.
    """

    if points == max_points:
        return "text-success"  # Green
    elif points == 0:
        return "text-danger"  # Red
    else:
        return "text-warning"  # Yellow


def test():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=69)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--brute", action="store_true")
    parser.add_argument("--src_dir", type=str, default=None)

    args = parser.parse_args()

    # Set the source directory
    src_dir = os.path.join(PROJECT_DIR, "src", "assignments")
    if args.brute and "UPLOAD_DIR" in os.environ:
        src_dir = os.path.join(os.environ["UPLOAD_DIR"], "assignments")
    elif args.src_dir is not None:
        src_dir = args.src_dir

    # Check if the source directory exists
    if not os.path.isdir(src_dir):
        RESULT["success"] = False
        RESULT["failure_message"] = "Expected a directory. Please check your zip file."
        print(RESULT["failure_message"])

    # Set the dataset directory
    if args.brute:
        dataset_dir = os.path.join(PROJECT_DIR, "data", "brute_tests")
        atexit.register(exit_handler, os.environ["UPLOAD_DIR"])
    else:
        dataset_dir = os.path.join(PROJECT_DIR, "data", "tests")

    # Check if the dataset directory exists
    if not os.path.isdir(dataset_dir):
        RESULT["success"] = False
        RESULT["failure_message"] = "Could not find the dataset directory."

    # Check if the modules exist
    for module in MODULES:
        module_name = f"assignments.{module}"
        module_path = os.path.join(src_dir, module + ".py")
        if not os.path.exists(module_path):
            RESULT["success"] = False
            RESULT["failure_message"] = f"Module file {module_name} could not be found."
            sys.exit(1)

    # Check if the modules can be imported and if the functions and classes exist
    try:
        from assignments.tuning import cross_validate_knn
        from assignments.knn_classifier import KNNClassifier
        from assignments.mlp_classifier import MLPClassifier
        from assignments.linear_classifier import LinearClassifier
    except Exception as e:
        RESULT["success"] = False
        RESULT["failure_message"] += f"Error while importing modules: {e}"
        sys.exit(1)

    print("\n================= TESTING ASSIGNMENTS =================\n")
    for assignment in create_assignments(dataset_dir):
        results = assignment.test_assignment(src_dir=src_dir, generate=args.generate, seed=args.seed)
        print(f"{assignment.name}: \n\t{results['message']}\n")
        color = text_color(results["points"], results["max_points"])

        RESULT[assignment.name] = results
        RESULT[assignment.name]["text_color"] = color

        RESULT["total_points"] += results["points"]

if __name__ == "__main__":
    test()
