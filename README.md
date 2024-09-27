# Label Approved

Label PRs that have been approved a number of times.

Inspired from [label-when-approved-action](https://github.com/abinoda/label-when-approved-action) but with support for PRs from forks.

## How to use

Install this GitHub action by creating a file in your repo at `.github/workflows/label-approved.yml`.

A minimal example could be:

```YAML
name: Label Approved

on:
  schedule:
    - cron: "0 0 * * *"

permissions:
  issues: write

jobs:
  label-approved:
    runs-on: ubuntu-latest
    steps:
    - uses: docker://tiangolo/label-approved:0.0.3
    # You can also use the action directly, but that will take about an extra minute:
    # - uses: tiangolo/label-approved@0.0.3
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
```

This example uses the defaults configurations.

It will run every night and check all the open PRs, for each PR with the label `awaiting-review`, it will check the approvals.

If there are 2 or more approvals, it will remove the label `awaiting-review` and will add the label `approved-2`.

## Configuration

You can add different labels to apply.

And for each label, you can specify:

* `number`: the minimum number of approvals.
* `await_label`: a label to filter the PRs. In the example above it is `awaiting-review` (the default when no configs are provided).
    * If `await_label` is omitted or `null`, it will apply to all open PRs.

These configs are passed as a JSON object, but as GitHub actions can only take strings as parameters, the JSON object has to be converted to a string.

Check the next example...

## Configuration Example

Here's an example with 3 labels to apply, each with its own config.

It's all inside of a single JSON config, passed as a multiline string.

In YAML (this format) you can use `>` to declare that a string has multiple lines.

```YAML
name: Label Approved

on:
  schedule:
    - cron: "0 0 * * *"

permissions:
  issues: write

jobs:
  label-approved:
    runs-on: ubuntu-latest
    steps:
    - uses: docker://tiangolo/label-approved:0.0.3
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        config: >
          {
            "approved-1":
              {
                "number": 1,
                "await_label": "awaiting-review"
              },
            "omg 2 approved":
              {
                "number": 2,
                "await_label": "only 2"
              },
            "approvals in 3D":
              {
                "number": 3
              }
          }
```

**Note**: Have in mind that after the `>` the multiline has to have at least one more level of indentation than the key `config` above.

Here's what this config will do:

Check each open PR, and:

* Apply the label `approved-1` to open PRs with:
    * 1 approval (or more).
    * The label `awaiting-review` (removing it afterwards).
* Apply the label `omg 2 approved` to open PRs with:
    * 2 approvals (or more).
    * The label `only 2` (removing it afterwards).
* Apply the label `approvals in 3D` to open PRs with:
    * 3 approvals (or more).
    * `await_label` was not declared, so, any open PR will match.

## Release Notes

### Latest Changes

#### Docs

* 📝 Update docs to use needed permissions for orgs. PR [#19](https://github.com/tiangolo/label-approved/pull/19) by [@tiangolo](https://github.com/tiangolo).

#### Internal

* ⬆ Bump docker/build-push-action from 2 to 5. PR [#10](https://github.com/tiangolo/label-approved/pull/10) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump docker/login-action from 1 to 3. PR [#12](https://github.com/tiangolo/label-approved/pull/12) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump docker/setup-buildx-action from 1 to 3. PR [#9](https://github.com/tiangolo/label-approved/pull/9) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Update `issue-manager.yml`. PR [#21](https://github.com/tiangolo/label-approved/pull/21) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update `latest-changes` GitHub Action. PR [#20](https://github.com/tiangolo/label-approved/pull/20) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add GitHub templates for discussions and issues, and security policy. PR [#18](https://github.com/tiangolo/label-approved/pull/18) by [@alejsdev](https://github.com/alejsdev).

### 0.0.4

#### Refactors

* ♻️ Rename default label from "awaiting review" to "awaiting-review". PR [#16](https://github.com/tiangolo/label-approved/pull/16) by [@tiangolo](https://github.com/tiangolo).

### 0.0.3

### Fixes

* ♻️ Upgrade Pydantic version and logic to handle GitHub providing env vars even without values. PR [#15](https://github.com/tiangolo/label-approved/pull/15) by [@tiangolo](https://github.com/tiangolo).

#### Internal

* 🔧 Add funding. PR [#13](https://github.com/tiangolo/label-approved/pull/13) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add dependabot. PR [#8](https://github.com/tiangolo/label-approved/pull/8) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add latest-changes GitHub Action. PR [#7](https://github.com/tiangolo/label-approved/pull/7) by [@tiangolo](https://github.com/tiangolo).

### 0.0.2

* 🐛 Fix approved user count logic. PR [#6](https://github.com/tiangolo/label-approved/pull/6) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix Python app name to be called in Docker. PR [#5](https://github.com/tiangolo/label-approved/pull/5) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade GitHub Action Latest Changes. PR [#4](https://github.com/tiangolo/label-approved/pull/4) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix logic to compute the number of approvals, count only last approval per user. PR [#3](https://github.com/tiangolo/label-approved/pull/3) by [@tiangolo](https://github.com/tiangolo).

### 0.0.1

First release 🎉

## License

This project is licensed under the terms of the MIT license.
