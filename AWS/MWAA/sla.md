Airflow SLAs at the task level are cummulative. The best way to think of the SLA is that it uses the "execution_date" on the task as its T-0. The execution_date on the task is the **"Data interval start"** on the dag.
On the "List SLA Misses" page, the "execution_date" is shown as the "Logical Date". The "Timestamp" column represents when the SLA was captured. SLAs are captured as they occur.

1. Pt_1.2 will fail as it has a SLA of 20 and it runs for 25 seconds
2. PT_1.1 will not fail SLA as it has an sla of 20, but runs for only 10 seconds
3. PT_2 will fail SLA, as even though it runs only for 20 seconds, its sla of 25 will be breached, because pt_1.2 takes 25 seconds to run and Pt_2 runs only after that.
4. PT_3.1 will pass SLA as it has an SLA of 65 and it should complete after (25+25+15=60) seconds.
5. PT_3.2 will fail SLA (sometimes) as it has an SLA of 60 and although it should complete in 60 seconds, it may not always do so
6. PT_3.4 is similar to PT_3.2 but will always pass, as it will complete at T+15 and its SLA is 60 seconds.
7. PT_3.5 has a short SLA but long duration. Although the task taskes 45 seconds to complete, the SLA is captured almost immediately after the SLA has expired.

![image](https://github.com/rajrao/mypublicnotes/assets/1643325/e417effe-47a0-4a97-9861-51571dbcbf66)


**SLA misses captured for the above DAG:**
![image](https://github.com/rajrao/mypublicnotes/assets/1643325/806e22b9-170c-47b2-951d-e5638959c767)




