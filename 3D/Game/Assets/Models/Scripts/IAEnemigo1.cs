using System;
using UnityEngine;

	[RequireComponent(typeof (UnityEngine.AI.NavMeshAgent))]
	[RequireComponent(typeof (Enemy1Character))]
	[RequireComponent(typeof (CharacterStats))]

	public class IAEnemigo1 : MonoBehaviour
	{
		public UnityEngine.AI.NavMeshAgent agent { get; private set; }             // the navmesh agent required for the path finding
		public Enemy1Character character { get; private set; } // the character we are controlling
		public CharacterStats stats;
		public Transform target;                                    // target to aim for
        public float lookRadius = 15f;
        public float distance=20f;
		public CharacterStats playerStats;

		private void Start()
		{
			// get the components on the object we need ( should not be null due to require component so no need to check )
			agent = GetComponentInChildren<UnityEngine.AI.NavMeshAgent>();
			character = GetComponent<Enemy1Character>();
			stats = GetComponent<CharacterStats>();
			agent.updateRotation = false;
			agent.updatePosition = true;
			playerStats = GameObject.FindWithTag ("Player").GetComponent<CharacterStats> ();
		}


		private void Update()
		{
			if (!stats.isDead ()) {
				if (target != null)
					distance = Vector3.Distance (target.position, transform.position);


				if (distance <= lookRadius) {
					agent.SetDestination (target.position);
					character.Move (agent.desiredVelocity, false, false);

					//Debug.Log("Radio inside");            

					if (distance < agent.stoppingDistance) {
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
