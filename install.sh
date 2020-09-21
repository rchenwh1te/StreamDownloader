echo 'Updating apt repositories'
sudo apt update
cd ~
echo 'Installing required dependencies...'
sudo apt install -y ffmpeg git python python-pip python3 python3-pip
echo 'Cloning source from Github...'
git clone https://github.com/rchenwh1te/StreamDownloader.git .StreamDownloader> /dev/null
echo Installing required python modules...
sudo python3 -m pip install -r StreamDownloader/requirements.txt
echo 'Which name do you want to use for this command?'
workingdirectory=$(pwd)
read CommandName
sudo echo alias $CommandName=\'python3 $workingdirectory/.StreamDownloader\' >> /home/*/.bashrc

echo Successfully installed StreamDownloader. Run the program using \'$CommandName\'. Thank you for installing our software.
source ~/.bashrc
