# Welcome interns!
This guide will give you an overview of how to get started working on the SAGE project.

## Part 1: Docker
For the SAGE project, the application [Docker](https://www.docker.com/) is being used extensively. Docker is a tool designed to make it easier to create, deploy, and run applications by using containers. Take some time to learn the fundamentals of Docker. Here's a link to a short and friendly tutorial: https://www.youtube.com/watch?v=7S73WERRqO4. Feel free to watch or use any resources to learn about Docker (ex. [https://docs.docker.com/](https://docs.docker.com/)). You will want to have [Docker Desktop](https://www.docker.com/get-started) installed to your computer.

## Part 2:  Account(s) Setup

### 1. Generate an SSH public key 
This must be the form of authentication that you use to SSH into any Argonne server. There is a good guide to generating a key [here](https://kb.iu.edu/d/aews).

### 2. Argonne Collaborator Account  
Skip this if you already have a Argonne Domain or Argonne Collaborator account.
https://apps.anl.gov/registration/collaborators

### 3. LCRC Account  
Needed to get access to upload your ML model, dataset, and our data store ( https://www.lcrc.anl.gov/for-users/getting-started/getting-an-account/ )

  1. Request membership to the `waggle` project by clicking "Join Project" on the right and then searching for waggle. Once your request has been approved (takes minutes or a few hours), you will also added automatically to the `lcrc` project. If not, let us know.
  2. Add your public SSH key to the LCRC account.

## Part 3: SSH Setup

Platform-specific instructions for configuing ssh clients can also be found here: [https://www.lcrc.anl.gov/for-users/getting-started/ssh/](https://www.lcrc.anl.gov/for-users/getting-started/ssh/)

### 1. Configure ./.ssh/config  

Add the following configuration to the file `~/.ssh/config` in you home folder on the machine that you will be using to login from: (It the file does not exist, create it.)

   ```text
   Host lcrc
      Hostname bebop.lcrc.anl.gov
      User USERNAME
   ```

   Replace `USERNAME` with your LCRC username. This defines the host `lcrc`.

### 2. Create .ssh/rsa_id  

Place your RSA private key (the one that came with your public key) into the `~/.ssh/rsa_id` file. This is where SSH will automatically pull your key from when you login.

### 3. Test ssh  

Run the command `ssh lcrc` to test your ability to log in to Bebop. IMPORTANT: If it asks you for a password in a prompt that looks like `Password:`, you have done something wrong (likely you did not setup an `id_rsa` file correctly). The server should only need your private key, not an additional password. If you try your Argonne password, it will reject it, and in my case, block me from very essential Argonne services.

### 4. Test waggle folder access  

In the Bebop SSH terminal, see if you can access the folder `/lcrc/project/waggle/summer_projects/summer2024`. If you cannot, Raj or Pete have not accepted your request to join the waggle project on LCRC. When you can access the folder, create a folder with you name and upload models and dataset you have been using in there with a document of description.
