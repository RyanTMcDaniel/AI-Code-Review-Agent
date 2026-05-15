import argparse
from agent import run_agent
from report import save_report

def main():
    parser = argparse.ArgumentParser(description="AI Code Review Agent")
    parser.add_argument("--repo", required=True, help="Path to the repository to review")
    parser.add_argument("--output", default="review_output.md", help="Output file path for the review")
    args = parser.parse_args()

    print(f'Starting review of {args.repo}...')

    result = run_agent(args.repo)
    save_report(result, args.output)

if __name__ == '__main__':
    main()