---
sidebar_position: 3
---

# ✂️ Configuring

## 📁 The `.autopr` Folder

When you initialize AutoPR for your repository, create a folder named `.autopr`.
Think of this directory as AutoPR's command center, where it looks for instructions on what to do.  
Inside this folder, there are a few important files and folders:

- `.autopr/triggers.yaml`: Tells AutoPR when to act.
- `.autopr/cache`: Where AutoPR stores its cache files.
  At the moment, action `prompt` (for executing LLM prompts) implements caching in the background.

Triggers serve as conditions or events that, when met, initiate specific actions,
such as pushing to a branch, or labeling a pull request.

## 🌊 Choosing some workflows to run

See [the workflows reference](../reference/workflows) for what workflows you can use. 
Copy the configuration provided into your `triggers.yaml` file and tweak it to your needs. 

## 🏁 Triggering custom actions

See [the triggers reference](../reference/triggers) for what triggers are available, 
and [the actions reference](../reference/actions) for what actions you can run.

See [the triggers example](../reference/triggers#-examples) for a few examples of how to configure triggers.

## 🚀 Ready, Set, Go!

And that's it! With your triggers set and workflows defined, AutoPR is ready to work its magic on your repository. 
Remember, you can always come back and tweak these configurations as your needs evolve. AutoPR is designed to be flexible and grow with you. 🌟

If you have any questions, or you need assistance with writing custom configuration, feel free to reach out to us on [Discord](https://discord.com/invite/ykk7Znt3K6) or [post an issue on Github](https://github.com/irgolic/AutoPR/issues).