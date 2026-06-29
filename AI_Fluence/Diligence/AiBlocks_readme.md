## superbase.com
* signup with Github accout
* Organization:RheinWeg
* GitHub: howardyang2009/aiblocks
* Project name: [Ai Blocks Project](https://supabase.com/dashboard/project/mvuzsjhqqggcccydflkv)
* Database password: BiWt2F29IBbJNMhS
* 0001_init.sql done.
* 0002_rls.sql done.

## clerk
* signup with Github account
* Project name: [AiBlocks](https://dashboard.clerk.com/apps/app_3FjXFeHwUKVblz3LB3blwFesHAl/instances/ins_3FjXFbq1prHl7WO9ydro638Rlk8)

## stripe
* sign-in with google account: howardyang2009@gmail.com
* business name: [RheinWeg](https://dashboard.stripe.com/acct_1TnDi42ELQtoolNT/test/dashboard)
* created one product gelbweiten-to-xlsx for one-off 10eur price
* create aiblocks-vercel-stripe-webhook
* [Stripe Test Credit Card](https://docs.stripe.com/testing#cards)
* go live [stripe](https://dashboard.stripe.com/acct_1TnDhsFzpUGk5t7K/dashboard) 
* create aiblocks-vercel-stripe-webhook again 
* add connected account https://aiblocks-six.vercel.app/dashboard/seller/stripe

## vercel
* sign-up with Github account
* Team name : RheinWeg
* Project name : [aiblocks](https://vercel.com/rhein-weg/aiblocks)
* deploy to https://aiblocks-six.vercel.app/

## testing
1. signin with Google account howardyang2009@gmail.com
2. publish gelbeseiten-to-xlsx.skill.zip
3. stripe payment and download process works fine
4. un-publish user checkout, download, and star works fine
5. deploy to vercel, in stripe, create aiblocks-vercel-stripe-webhook, redeploy
6. first payment to go live stripe connected account works fine

## open questions
- [ ] how a seller connect their stripe account to our stripe account, whether they really need one stripe account, or maybe they just do stripe connected account onboarding and during publish components, they just provide their Bank account info. then we send they earned money to their bank account every week?
