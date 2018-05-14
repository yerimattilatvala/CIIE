using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof (UnityEngine.AI.NavMeshAgent))]
[RequireComponent(typeof (BossCharacter))]
[RequireComponent(typeof (CharacterStats))]


public class IABoss : MonoBehaviour {

		public UnityEngine.AI.NavMeshAgent agent { get; private set; }             // the navmesh agent required for the path finding
		public BossCharacter character { get; private set; } // the character we are controlling
		public CharacterStats stats;
		public Transform target;                                    // target to aim for
		public float lookRadius = 15f;
		public float distance=20f;
		public CharacterStats playerStats;
		public GameObject shield;
		private Vector3 pos2;
	private int lastCurrentHealth;
	private float y1;
	private bool activate = false;

		private void Start()
		{
			// get the components on the object we need ( should not be null due to require component so no need to check )
			target=GameObject.FindGameObjectWithTag("Player").transform;
			agent = GetComponentInChildren<UnityEngine.AI.NavMeshAgent>();
			character = GetComponent<BossCharacter>();
			stats = GetComponent<CharacterStats>();
			agent.updateRotation = false;
			agent.updatePosition = true;
			playerStats = GameObject.FindWithTag ("Player").GetComponent<CharacterStats> ();
			lastCurrentHealth = stats.currentHealth;
			pos2=GameObject.FindWithTag ("HandBoss").transform.position;
		y1 = shield.transform.position.y;
			}

	private void Update (){
	}
		private void FixedUpdate()
		{
		if (activate) {
			pos2 = GameObject.FindWithTag ("HandBoss").transform.position;
			shield.transform.position = pos2-new Vector3(0.3f,1.5f,0.2f);

			if (!stats.isDead ()) {
				if (target != null)
				if (agent.remainingDistance < agent.stoppingDistance) {

					activate = false;	
					lastCurrentHealth = stats.currentHealth;
					pos2.y = y1;
					shield.transform.position = pos2 + new Vector3(0.6f,-0.5f,2.3f);

					shield.transform.localRotation *= Quaternion.Euler (0, 180, 0);
					// Debug.Log("Attack");
				}
			} else {
				character.Die ();
				agent.isStopped = true;
			}
		}else {
			if (!stats.isDead ()) {
				if (target != null)
					distance = Vector3.Distance (target.position, transform.position);
					
				if (stats.currentHealth < (lastCurrentHealth - 30)) {
					character.Protected ();
					activate = true;
					shield.transform.localRotation *= Quaternion.Euler (0, 180, 0);
				} else if (distance <= lookRadius) {
					//pos1 = shield.transform.position;
					agent.SetDestination (target.position);
					character.Move (agent.desiredVelocity, false, false);

					//Debug.Log("Radio inside");            
					if (agent.remainingDistance < agent.stoppingDistance) {	
						character.Attack ();
						// Debug.Log("Attack");
					}
				} else {
					agent.SetDestination (agent.transform.localPosition);
					character.Move (Vector3.zero, false, false);
					//Debug.Log("Idle");
				}
			} else {
				character.Die ();
				agent.isStopped = true;
			}
		}
		}

		public void SetTarget(Transform target)
		{
			this.target = target;
		}

		void OnDrawGizmosSelected()
		{
			Gizmos.color = Color.red;
			Gizmos.DrawWireSphere(transform.position, lookRadius);
		}


	}
