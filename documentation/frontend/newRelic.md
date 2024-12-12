# Background

New Relic is a monitoring platform, used by the Simpler Grants team to:

- keep track of system performance across the full application
- track and visualize some product metrics
- generate alerts? (tbd)

New Relic UI is available at [https://one.newrelic.com/](https://one.newrelic.com/).

# Apps and Accounts

New Relic will be installed to monitor the following in DEV, Staging, and PROD environments:

- Next JS client and backend
- API (tbd)
- Infrastructure (tbd)

Each deployed application / environment combination will have its own name to distinguish it, but all applications will reference the same license key (found in 1password).

The Simpler Grants team will have licenses for 4 admin users, 5 non-admin users. If you need access, please consult with your manager.

(TBD - section on what admins / non-admins have access to)

# Usage

TBD - what are important features to know about, and how do we use them?

## Dashboards

TBD

# Integration

Note that all integrations will require access to two pieces of information:

- `NEW_RELIC_APP_NAME`
- `NEW_RELIC_LICENSE_KEY`

## Next JS

### Local

Generally you should not need run New Relic locally. By default `npm run dev` will run with the `NEW_RELIC_ENABLED` flag set to `false`. If you need to run the app with New Relic locally, run without this flag, and supply the `NEW_RELIC_APP_NAME` and `NEW_RELIC_LICENSE_KEY` variables via the command line when you start the app.

For testing locally in order to more closely emulate the deployed environment, see the considerations mentioned in the `deployed` section below.

### Deployed

**Note:** This section is TBD as we work through some issues with our New Relic implementation for the Next client.

Integration of New Relic into the client and Node processes will be handled by the New Relic Node package. The Node library is able to generate the necessary scripts for the client code to report back to New Relic. [See the layout file](https://github.com/HHS/simpler-grants-gov/blob/a2ce07dc15b65c9fa27ecbbe7a9566c84542b554/frontend/src/app/%5Blocale%5D/layout.tsx#L77) to see how this is being done.

Unfortunately, due to the issues below, this gets complicated with our Next JS setup.

#### Environment Variables

Environment variables containing the necessary New Relic configuration values (see above) for deployed environments are stored in SSM parameters and supplied to the app via ECS task definitions at the Next application's run time. (For more about the application's environments, [check documentation here](https://github.com/HHS/simpler-grants-gov/blob/main/documentation/frontend/environments.md)).

### Known Issues / Troubleshooting

- When adding the New Relic snippet code to the Grants codebase manually, you will need to double escape any backslashes, as single backslashes are removed at some point in the build process. Failure to add the extra backslashes will cause the script to fail.

- New Relic browser monitoring is inconsistent in our current implementation.

- Since the app name and license key are supplied to the Next app at run time, while APM monitoring will work fine, any code that is rendered at build time will not have access to the configuration, meaning that client monitoring is more tricky. We are trying to work with New Relic on a solution.

- As our client side code expects New Relic configuration to be available when running `npm run build`, we will see warnings in our build logs related to this missing data.

- The Typescript types package for New Relic's Node implementation is lacking a bit. We are working around this in our code, but there is a ticket out to contribute back to the New Relic package as well so that we do not need to manage this ourselves. See https://github.com/HHS/simpler-grants-gov/issues/2982

- client side error: `ChunkLoadError: Loading chunk 478 failed.`
  - FIX: this happens locally when the script is blocked. Firefox tends to block, try running in Chrome.

### Resources

Here are some resources to reference when setting up or using New Relic on Next

- [New Relic NPM Package](https://www.npmjs.com/package/newrelic) - some setup directions here
- [Next JS Sample App](https://github.com/newrelic/newrelic-node-examples/tree/58f760e828c45d90391bda3f66764d4420ba4990/nextjs-app-router) - generally tried to follow this example when setting up our implementation
- [New Relic's installation guide for Node](https://docs.newrelic.com/docs/apm/agents/nodejs-agent/installation-configuration/install-nodejs-agent-docker/)
