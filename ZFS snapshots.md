## January 19, 2024 11:53 AM
- Below is a Bash script that automates the creation of ZFS snapshots and sends them to a remote server. This script assumes that you have a ZFS pool and dataset already set up, and that you have SSH access to the remote server where you want to send the snapshots.
  title:: ZFS snapshots
- ### Script: `zfs_snapshot_and_send.sh`
  
  ```bash
  #!/bin/bash
  
  # Configuration
  LOCAL_POOL="your_pool"                  # Local ZFS pool name
  REMOTE_USER="remote_user"               # Remote server username
  REMOTE_HOST="remote_host"               # Remote server hostname or IP
  REMOTE_PATH="/path/to/remote/backup"    # Path on the remote server to store the snapshots
  SNAPSHOT_PREFIX="backup"                # Prefix for the snapshot names
  DATE_FORMAT="+%Y-%m-%d_%H-%M-%S"       # Date format for snapshot names
  
  # Create snapshot name based on the current date and time
  TIMESTAMP=$(date "$DATE_FORMAT")
  SNAPSHOT_NAME="${SNAPSHOT_PREFIX}_${TIMESTAMP}"
  
  # Create the ZFS snapshot
  echo "Creating ZFS snapshot ${LOCAL_POOL}@${SNAPSHOT_NAME}..."
  zfs snapshot "${LOCAL_POOL}@${SNAPSHOT_NAME}"
  
  # Check if the snapshot creation was successful
  if [ $? -ne 0 ]; then
  echo "Error: Failed to create ZFS snapshot."
  exit 1
  fi
  
  # Send the snapshot to the remote server
  echo "Sending snapshot ${LOCAL_POOL}@${SNAPSHOT_NAME} to remote server..."
  zfs send "${LOCAL_POOL}@${SNAPSHOT_NAME}" | ssh "${REMOTE_USER}@${REMOTE_HOST}" "cat > ${REMOTE_PATH}/${SNAPSHOT_NAME}.zfs"
  
  # Check if the snapshot transfer was successful
  if [ $? -ne 0 ]; then
  echo "Error: Failed to send snapshot to remote server."
  exit 1
  fi
  
  # Optionally, you can remove the local snapshot after sending
  # Uncomment the following line if you want to delete the snapshot locally
  # zfs destroy "${LOCAL_POOL}@${SNAPSHOT_NAME}"
  
  echo "Snapshot ${SNAPSHOT_NAME} created and sent successfully."
  ```
- ### Instructions:
  
  1. **Edit the Script:**
	- Replace `your_pool` with the name of your ZFS pool.
	- Replace `remote_user`, `remote_host`, and `/path/to/remote/backup` with the appropriate values for your remote server and backup path.
	- Adjust `SNAPSHOT_PREFIX` and `DATE_FORMAT` to suit your preferences for naming snapshots.
	  
	  2. **Make the Script Executable:**
	  ```bash
	  chmod +x zfs_snapshot_and_send.sh
	  ```
	  
	  3. **Run the Script:**
	  ```bash
	  ./zfs_snapshot_and_send.sh
	  ```
- ### Notes:
- Ensure that `ssh` access to the remote server is set up and that you have the necessary permissions to write to the specified remote path.
- If you want to include additional features (like rotating snapshots or handling errors in more detail), you can expand on this basic script.
- Be cautious with the snapshot deletion step. Make sure you really want to remove local snapshots before uncommenting the `zfs destroy` command.