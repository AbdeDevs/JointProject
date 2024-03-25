from github import Github
import matplotlib.pyplot as plt
import datetime
from generate_histogram import token, repo_name, labels_count
import argparse

g = Github(token)
repo = g.get_repo(repo_name)


def get_date_range_of_current_week() -> tuple:
    """Gets the date range of the current week from Monday to Sunday as datetime objects."""
    current_date = datetime.datetime.now()
    start_of_week = current_date - datetime.timedelta(days=current_date.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)
    start_of_week = datetime.datetime.combine(start_of_week.date(), datetime.datetime.min.time())
    end_of_week = datetime.datetime.combine(end_of_week, datetime.datetime.max.time())
    return start_of_week, end_of_week


def count_labels(state="open") -> None:
    """Counts the number of issues with each label, filtering for the current week."""
    start_of_week, end_of_week = get_date_range_of_current_week()
    issues = repo.get_issues(state="all", since=start_of_week)

    for issue in issues:
        if issue.created_at <= end_of_week:
            if issue.state == state and \
               ((state == "open" and issue.created_at >= start_of_week) or \
               (state == "closed" and issue.closed_at is not None and issue.closed_at >= start_of_week)):
                for label in issue.labels:
                    if label.name in labels_count:
                        labels_count[label.name] += 1


def generate_plot(state="open") -> None:
    """Generates a histogram of the number of issues with each label."""
    plt.figure(figsize=(10, 6))
    plt.bar(labels_count.keys(), labels_count.values())
    plt.ylabel(f'Number of Issues ({state})')
    plt.title(f'Histogram of Issues ({state}) by Label - {get_date()}')
    plt.xticks(rotation=20)
    plt.yticks(range(0, max(labels_count.values()) + 1))
    plt.savefig(f"histogram_issues_{state}.png")


def get_date() -> str:
    """The format is: MX-WY-Report -> where X is the month number and Y is the week number"""
    now = datetime.datetime.now()
    month = now.strftime("%m")
    week_of_year = int(now.strftime("%U"))
    first_day_of_month = now.replace(day=1)
    week_of_first_day = int(first_day_of_month.strftime("%U"))
    week_of_month = week_of_year - week_of_first_day + 1
    return f"M{month}-W{week_of_month}-Report"


def parse_args() -> argparse.Namespace:
    """Parses the arguments for the script."""
    parser = argparse.ArgumentParser(
        description='Generates a histogram of the number of issues with each label')
    parser.add_argument('--state', choices=['open', 'closed', 'all'], default='open',
                        help='The state of the issues being gathered')
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.state:
        count_labels(state=args.state)
        generate_plot(state=args.state)
    else:
        count_labels()
        generate_plot()


if __name__ == '__main__':
    main()
